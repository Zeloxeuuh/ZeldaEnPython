from dataclasses import dataclass

import pygame
import pyscroll
import pytmx

from player import NPC


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]

class MapManager:
    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "Cocorico"

        # Enregistrement des maps
        self.register_map("Cocorico", portals=[

            Portal(from_world="Cocorico", origin_point="enter_house", target_world="HouseLink", teleport_point="spawn_house"),
            Portal(from_world="Cocorico", origin_point="enter_shop", target_world="CocoricoShop", teleport_point="spawn_shop"),
            Portal(from_world="Cocorico", origin_point="enter_armorer", target_world="CocoricoArmorer", teleport_point="spawn_armorer")

        ], npcs=[
            NPC("Robin", nb_points=4, dialog=["EH ! Link, ta mamie t'appelle depuis tout à l'heure",
                                                    "Vas la voir ! ",
                                                    "Elle t'attends dans ta maison."], enemy=False)
        ])

        self.register_map("HouseLink", portals=[
            Portal(from_world="HouseLink", origin_point="exit_house", target_world="Cocorico", teleport_point="enter_house_exit")
        ], npcs=[
            NPC("Paul", nb_points=2, dialog=["Linkkkkkk, Mamie c'est fait enlevé",], enemy=False)
        ])

        self.register_map("CocoricoShop", portals=[
            Portal(from_world="CocoricoShop", origin_point="exit_shop", target_world="Cocorico", teleport_point="enter_shop_exit")
        ])

        self.register_map("CocoricoArmorer", portals=[
            Portal(from_world="CocoricoArmorer", origin_point="exit_armorer", target_world="Cocorico", teleport_point="enter_armorer_exit")
        ])

        self.teleport_player("player")
        self.teleport_npcs()

    def check_npc_collision(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)

    def check_collision(self):
        # Portals
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # Charger la carte classique
        if portals is None:
            portals = []
        tmx_data = pytmx.util_pygame.load_pygame(f"Maps/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2.3

        # Les collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        # Add les npcs au groupe
        for npc in npcs:
            group.add(npc)

        # Crée un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for maps in self.maps:
            map_data = self.maps[maps]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collision()

        for npc in self.get_map().npcs:
            npc.move()