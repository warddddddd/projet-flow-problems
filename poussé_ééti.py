from affichage import afficher_matrice

def pousser_reetiqueter(capacites, source, puits):

    n = len(capacites)
    hauteur = [0] * n
    excedent = [0] * n
    residuel = [ligne[:] for ligne in capacites]

    def pousser(u, v):
        if hauteur[u] == hauteur[v] + 1:
            delta = min(excedent[u], residuel[u][v])
            residuel[u][v] -= delta
            residuel[v][u] += delta
            excedent[u] -= delta
            excedent[v] += delta
            print(f"Poussé {delta} unités de {u} à {v}")

    def reetiqueter(u):
        hauteur_min = float('inf')
        for v in range(n):
            if residuel[u][v] > 0:
                hauteur_min = min(hauteur_min, hauteur[v])
        hauteur[u] = hauteur_min + 1
        print(f"Réétiqueté sommet {u} à hauteur {hauteur[u]}")

    # Initialisation du préflot
    hauteur[source] = n
    excedent[source] = 0
    for v in range(n):
        if capacites[source][v] > 0:
            flot = capacites[source][v]
            residuel[source][v] = 0
            residuel[v][source] = flot
            excedent[v] = flot
            excedent[source] -= flot

    print("Initialisation complète (Pousser-Réétiqueter)")
    print(f"Hauteurs: {hauteur}")
    print(f"Excédents: {excedent}")
    afficher_matrice(residuel, "Matrice résiduelle initiale")

    actifs = [i for i in range(n) if i != source and i != puits and excedent[i] > 0]

    iteration = 0  # Compteur d'itérations
    while actifs:
        iteration += 1
        u = actifs.pop(0)
        dechargement_termine = False
        while excedent[u] > 0 and not dechargement_termine:
            pousse_effectue = False
            for w in range(n):
                if residuel[u][w] > 0 and hauteur[u] == hauteur[w] + 1:
                    pousser(u, w)
                    pousse_effectue = True
                    if w != source and w != puits and excedent[w] > 0 and w not in actifs:
                        actifs.append(w)
                    if excedent[u] == 0:
                        dechargement_termine = True
                        break
            if not pousse_effectue and excedent[u] > 0:
                reetiqueter(u)
        if excedent[u] > 0 and u != source and u != puits and u not in actifs:
            actifs.append(u)

        # Affichage des informations après cette itération
        print(f"\n*** Itération {iteration} ***")
        print(f"Hauteurs: {hauteur}")
        print(f"Excédents: {excedent}")
        afficher_matrice(residuel, "Matrice résiduelle après cette itération")
        print()  # Saut de ligne pour séparer les itérations

    flot_max = sum(capacites[source][v] - residuel[source][v] for v in range(n))
    return flot_max
