import pygame
import pytmx
import pyscroll

from map import MapManager
from player import Player
from dialog import DialogBox
from inventaire import Inventaire

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

            # if rect_x > final_x:
            #     rect_x -= speed
            # else:
            #     rect_x = final_x

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

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
