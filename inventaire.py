import pygame

class Inventaire:
    def __init__(self, screen, width, height, row, col):
        self.screen = screen
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.slot_size = 50
        self.slot_spacing = 10
        self.slots = None
        self.bg_inv = None
        self.inventaire_ouvert = False
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # Background inventaire
        self.initial_x = 1280
        self.final_x = 940
        self.rect_x = self.initial_x

        # Slots inventaire
        self.initial_slot_x = 1280
        self.final_slot_x = 940
        self.rect_slot_x = self.initial_slot_x

        self.speed = 7

    def slot(self, x, y):
        self.slots = pygame.draw.rect(self.screen, self.white, (x, y, self.slot_size, self.slot_size), 2)

    def background(self):

        # Animation
        if self.inventaire_ouvert:
            if self.rect_x > self.final_x:
                self.rect_x -= self.speed
            else:
                self.rect_x = self.final_x

        self.bg_inv = pygame.draw.rect(self.screen, self.black, (self.rect_x, 80, self.width - 40, self.height - 40))

    def draw_slot(self):

        # Animation
        if self.inventaire_ouvert:
            if self.rect_slot_x > self.final_slot_x:
                self.rect_slot_x -= self.speed
            else:
                self.rect_slot_x = self.final_slot_x

        for row in range(self.row):
            for col in range(self.col):
                x = col * (self.slot_size + self.slot_spacing)
                y = row * (self.slot_size + self.slot_spacing)
                self.slot(x + self.rect_slot_x + 25, y + 205)

    def draw_inventory(self):
        if self.inventaire_ouvert:
            self.background()
            self.draw_slot()

        # Reset de l'animation
        if not self.inventaire_ouvert:
            self.rect_x = self.initial_x
            self.rect_slot_x = self.initial_slot_x