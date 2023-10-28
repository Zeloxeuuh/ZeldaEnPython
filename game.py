import pygame
import pytmx
import pyscroll

from map import MapManager
from player import Player
from dialog import DialogBox
from inventaire import Item, Inventaire

class Game:
    def __init__(self):
        # Fenêtre du jeu
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("The Legend of Zelda Python of the world")

        # Générer un joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox()
        self.inventaire = Inventaire(self.screen, 380, 600, 7, 5)

        # Initialisiation des Items
        self.apple = Item("Pomme", "Assets/Item/Item_apple.png", "Une délicieuse pomme", stackable=True, size=(60, 55))
        self.bombe = Item("Bombe", "Assets/Item/Item_bombe.png", "Une puissante épée", stackable=True, size=(40, 40))

        # Potions
        self.empty_potion = Item("Fiole vide", "Assets/Item/Item_empty_potion.png", "Une fiole vide", stackable=True, size=(40, 40))
        self.endurence_potion = Item("Fiole d'endurence", "Assets/Item/Item_endurence_potion.png", "Une fiole remplie d'un composant vert", stackable=True, size=(40, 40))
        self.heal_potion = Item("Fiole de vie", "Assets/Item/Item_heal_potion.png", "Une fiole remplie d'un composant rouge", stackable=True, size=(40, 40))
        self.strenght_potion = Item("Fiole de force", "Assets/Item/Item_strenght_potion.png", "Une fiole remplie d'un composant bleu", stackable=True, size=(40, 40))

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
            self.inventaire.draw_inventory()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Quand on appuie sur une touche
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.map_manager.check_npc_collision(self.dialog_box)
                    elif event.key == pygame.K_o:
                        self.player.damage(0.5)
                    elif event.key == pygame.K_i:
                        self.inventaire.inventaire_ouvert = not self.inventaire.inventaire_ouvert
                    elif event.key == pygame.K_a:
                        self.inventaire.add_item(self.apple)
                    elif event.key == pygame.K_b:
                        self.inventaire.add_item(self.bombe)
                    elif event.key == pygame.K_h:
                        self.inventaire.add_item(self.heal_potion)
                    elif event.key == pygame.K_e:
                        self.inventaire.add_item(self.empty_potion)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
