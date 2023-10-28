import pygame

class Item:
    def __init__(self, name, image_path, description, stackable=False, size=(1, 1)):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.description = description
        self.stackable = stackable
        self.quantity = 1 if stackable else 0
        self.size = size

class Inventaire:
    def __init__(self, screen, width, height, row, col):
        self.screen = screen
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.slot_size = 50
        self.slot_spacing = 10
        self.slots = []
        self.items = [[None for _ in range(col)] for _ in range(row)]
        self.bg_inv = None
        self.data_bg = None
        self.inventaire_ouvert = False
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.grey = (100, 100, 100)
        self.font = pygame.font.Font(None, 24)

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
        slot_rect = pygame.draw.rect(self.screen, self.white, (x, y, self.slot_size, self.slot_size), 2, border_radius=15)
        self.slots.append(slot_rect)

    def background(self):
        # Animation
        if self.inventaire_ouvert:
            if self.rect_x > self.final_x:
                self.rect_x -= self.speed
            else:
                self.rect_x = self.final_x

        self.bg_inv = pygame.draw.rect(self.screen, self.white, (self.rect_x, 80, self.width - 40, self.height - 40), border_top_left_radius=15, border_bottom_left_radius=15)
        self.data_bg = pygame.draw.rect(self.screen, self.black, (self.rect_x, 80, self.width - 40, self.height - 500), border_top_left_radius=15)

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
                pygame.draw.rect(self.screen, self.black, (x + self.rect_slot_x + 25, y + 205, self.slot_size, self.slot_size), 2, border_radius=15)

    def draw_inventory(self):
        if self.inventaire_ouvert:
            self.background()
            self.draw_slot()
            self.draw_items()

        # Reset de l'animation
        if not self.inventaire_ouvert:
            self.rect_x = self.initial_x
            self.rect_slot_x = self.initial_slot_x

    def draw_items(self):
        for row in range(self.row):
            for col in range(self.col):
                item = self.items[row][col]
                if item is not None:
                    item_x = self.rect_slot_x + 25 + col * (self.slot_size + self.slot_spacing)
                    item_y = 205 + row * (self.slot_size + self.slot_spacing)
                    scaled_image = pygame.transform.scale(item.image, item.size)
                    centered_x = item_x + (self.slot_size - item.size[0]) // 2
                    centered_y = item_y + (self.slot_size - item.size[1]) // 2
                    self.screen.blit(scaled_image, (centered_x, centered_y - 1))
                    if item.stackable and item.quantity > 1:
                        text = self.font.render(str(item.quantity), True, self.black)
                        self.screen.blit(text, (item_x + self.slot_size - 30, item_y + self.slot_size - 30))

    def add_item(self, item):
        for row in range(self.row):
            for col in range(self.col):
                if self.items[row][col] is None:
                    self.items[row][col] = item
                    return
                elif self.items[row][col].name == item.name and self.items[row][col].stackable:
                    self.items[row][col].quantity += 1
                    return