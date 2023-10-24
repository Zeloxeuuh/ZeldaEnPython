import pygame

class Item:
    def __init__(self, nom, image, description):
        self.nom = nom
        self.image = image
        self.description = description

class Slot:
    def __init__(self, x, y, largeur, hauteur):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.objet = None
        self.full = False

    def afficher(self, fenetre):
        pygame.draw.rect(fenetre, (0, 0, 0), self.rect, 2)
        if self.objet:
            fenetre.blit(self.objet.image, (self.rect.x, self.rect.y))

class Inventaire:
    def __init__(self, largeur, hauteur, nb_lignes, nb_colonnes):
        self.largeur = largeur
        self.hauteur = hauteur
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.slots = []

        slot_x = 50
        slot_y = 50
        slot_largeur = 100
        slot_hauteur = 100

        for lig in range(nb_lignes):
            for col in range(nb_colonnes):
                self.slots.append(Slot(slot_x, slot_y, slot_largeur, slot_hauteur))
                slot_x += slot_largeur + 10
            slot_x = 50
            slot_y += slot_hauteur + 10

        self.inventaire_ouvert = False

    def afficher(self, fenetre):
        if self.inventaire_ouvert:
            pygame.draw.rect(fenetre, (255, 255, 255), (20, 20, self.largeur - 40, self.hauteur - 40))

            for slot in self.slots:
                slot.afficher(fenetre)

    def add_to_inventory(self, objet, inventaire):
        for slot in inventaire.slots:

            if not slot.full:
                print(inventaire.slots)
                slot.objet = objet
                slot.full = True
                break
