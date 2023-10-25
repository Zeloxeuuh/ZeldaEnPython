import pygame

class Item:
    def __init__(self, nom, image, description):
        self.nom = nom
        self.image = image
        self.description = description
        self.rect = self.image.get_rect()

class Slot:
    def __init__(self, x, y, largeur, hauteur):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.objet = None
        self.full = False

    def afficher(self, fenetre):
        pygame.draw.rect(fenetre, (0, 0, 0), self.rect, 2)
        if self.objet:
            fenetre.blit(pygame.transform.scale(self.objet.image, (64, 64)), (self.rect.x + 7.5, self.rect.y + 7))

class Inventaire:
    def __init__(self, largeur, hauteur, nb_lignes, nb_colonnes):
        self.largeur = largeur
        self.hauteur = hauteur
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.slots = []
        self.inventaire_ouvert = False

        slot_x = 310
        slot_y = 180
        slot_largeur = 80
        slot_hauteur = 80

        for lig in range(nb_lignes):
            for col in range(nb_colonnes):
                self.slots.append(Slot(slot_x, slot_y, slot_largeur, slot_hauteur))
                slot_x += slot_largeur + 10
            slot_x = 310
            slot_y += slot_hauteur + 10

    def afficher(self, fenetre):
        if self.inventaire_ouvert:
            pygame.draw.rect(fenetre, (255, 255, 255), (280, 150, self.largeur - 40, self.hauteur - 40))

            for slot in self.slots:
                slot.afficher(fenetre)

    def add_to_inventory(self, objet, inventaire):
        for slot in inventaire.slots:

            if not slot.full:
                print(inventaire.slots)
                slot.objet = objet
                slot.full = True
                break

    def remove_inventory(self, objet, inventaire):
        pass
