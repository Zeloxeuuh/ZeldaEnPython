import pygame

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Inventaire avec Pygame")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Classe pour les objets
class Item:
    def __init__(self, nom, image, description):
        self.nom = nom
        self.image = image
        self.description = description

# Classe pour les slots
class Slot:
    def __init__(self, x, y, largeur, hauteur):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.objet = None
        self.rempli = False

    def afficher(self, fenetre):
        pygame.draw.rect(fenetre, BLANC, self.rect, 2)
        if self.objet:
            fenetre.blit(self.objet.image, (self.rect.x, self.rect.y))

# Classe pour l'inventaire
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

        for _ in range(nb_lignes):
            for _ in range(nb_colonnes):
                self.slots.append(Slot(slot_x, slot_y, slot_largeur, slot_hauteur))
                slot_x += slot_largeur + 10
            slot_x = 50
            slot_y += slot_hauteur + 10

        self.inventaire_ouvert = False

    def afficher(self, fenetre):
        if self.inventaire_ouvert:
            pygame.draw.rect(fenetre, NOIR, (20, 20, self.largeur - 40, self.hauteur - 40))

            for slot in self.slots:
                slot.afficher(fenetre)

    def ajouter_objet_a_inventaire(objet, inventaire):
        for slot in inventaire.slots:
            if not slot.rempli:
                slot.objet = objet
                slot.rempli = True
                break


# Liste pour stocker tous les objets créés
objets_crees = []

# Fonction pour créer un nouvel objet
def creer_objet(nom, image, description):
    nouvel_objet = Item(nom, image, description)
    objets_crees.append(nouvel_objet)
    return nouvel_objet


# Création d'objets
objet1 = creer_objet("Épée", pygame.image.load("Assets/Item/Item_rubis_green.png"), "Une puissante épée")
objet2 = creer_objet("Potion", pygame.image.load("Assets/Item/Item_rubis_green.png"), "Une potion magique")

# Création de l'inventaire
inventaire = Inventaire(largeur, hauteur, 4, 3)

# Boucle principale
en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                inventaire.inventaire_ouvert = not inventaire.inventaire_ouvert
            elif event.key == pygame.K_c:
                # Crée un nouvel objet et ajoute-le à l'inventaire
                Inventaire.ajouter_objet_a_inventaire(objet1, inventaire)

    fenetre.fill(NOIR)

    # Affichage de l'inventaire
    inventaire.afficher(fenetre)

    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()