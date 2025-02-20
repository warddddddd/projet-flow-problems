def lire_fichier_flots(nom_fichier):

    with open(nom_fichier, 'r') as fichier:
        # Lire le nombre de sommets
        ligne = fichier.readline().strip()
        if not ligne:
            raise ValueError("Fichier vide ou format incorrect.")
        n = int(ligne)

        # Lire la matrice de capacités
        capacites = []
        for _ in range(n):
            ligne = fichier.readline()
            if not ligne:
                raise ValueError("Le fichier ne contient pas assez de lignes pour la matrice des capacités.")
            ligne_split = list(map(int, ligne.strip().split()))
            if len(ligne_split) != n:
                raise ValueError("Les lignes de la matrice des capacités ne contiennent pas exactement n valeurs.")
            capacites.append(ligne_split)

        # Tenter de lire la matrice des coûts
        position_actuelle = fichier.tell()
        lignes_couts = []
        for _ in range(n):
            ligne = fichier.readline()
            if not ligne:
                # Pas assez de lignes pour la matrice de coûts
                fichier.seek(position_actuelle)
                lignes_couts = []
                break
            ligne_split = list(map(int, ligne.strip().split()))
            if len(ligne_split) != n:
                # Matrice de coûts non valide
                fichier.seek(position_actuelle)
                lignes_couts = []
                break
            lignes_couts.append(ligne_split)

        couts = lignes_couts if len(lignes_couts) == n else None

    return n, capacites, couts

def afficher_matrice(matrice, titre):
    """
    Affiche une matrice avec un alignement soigné, sans trop d'écarts.
    """
    print(f"\n{titre}:")
    largeur_col = max(len(str(val)) for ligne in matrice for val in ligne)
    for ligne in matrice:
        print(" ".join(f"{val:>{largeur_col}}" for val in ligne))

def afficher_matrices(capacites, couts=None, table_bellman=None):
    """
    Affiche soigneusement la matrice des capacités, des coûts (si applicable),
    et la table de Bellman (si applicable).
    """
    afficher_matrice(capacites, "Matrice des capacités")

    if couts is not None:
        afficher_matrice(couts, "Matrice des coûts")
    # La table de Bellman est déjà affichée dans bellman_ford si nécessaire.
