import pygame
import pytmx
import pyscroll

from map import MapManager
from player import Player
from dialog import DialogBox
from inventaire import Inventaire, Item, Slot


class Game:
    def __init__(self):
        # Fenêtre du jeu
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("The Legend of Zelda Python of the world")

        # Générer un joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox()
        self.new_object = []
        self.inventaire = Inventaire(1040, 720, 4, 5)

        # Initialisation des objets
        self.green_rubis = self.create_item("Rubis vert", pygame.image.load("Assets/Item/Item_rubis_green.png"), "Ce rubis est seul")
        self.bombe = self.create_item("Bombe", pygame.image.load("Assets/Item/Item_bombe.png"), "BOUM")

    def create_item(self, nom, image, description):
        new_item = Item(nom, image, description)
        self.new_object.append(new_item)
        return new_item

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_z]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.player.move_right()

    def update(self):
        self.map_manager.update()

    def run(self):

        clock = pygame.time.Clock()

        # Boucle du jeu
        running = True
        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            self.player.draw_hud(self.screen)
            self.inventaire.afficher(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.map_manager.check_npc_collision(self.dialog_box)
                    elif event.key == pygame.K_o:
                        self.player.damage(0.5)
                    elif event.key == pygame.K_e:
                        self.inventaire.inventaire_ouvert = not self.inventaire.inventaire_ouvert
                    elif event.key == pygame.K_g:
                        # Crée un nouvel objet et ajoute-le à l'inventaire
                        Inventaire.add_to_inventory(self, self.bombe, self.inventaire)

            clock.tick(60)

        pygame.quit()
