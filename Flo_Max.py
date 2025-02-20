from affichage import afficher_matrice

def ford_fulkerson(capacites, source, puits):
    """
    Implémente l'algorithme de Ford-Fulkerson pour trouver le flot maximal.
    """
    n = len(capacites)
    flot = 0
    residuel = [ligne[:] for ligne in capacites]

    def afficher_matrice_residuelle(matrice):
        afficher_matrice(matrice, "Matrice résiduelle après mise à jour")

    def bfs():
        parent = [-1] * n
        visite = [False] * n
        file = [source]
        visite[source] = True

        while file:
            u = file.pop(0)
            for v in range(n):
                if not visite[v] and residuel[u][v] > 0:
                    parent[v] = u
                    visite[v] = True
                    if v == puits:
                        return parent
                    file.append(v)
        return None

    while True:
        chemin = bfs()
        if not chemin:
            break

        v = puits
        flot_chaine = float('inf')
        arcs_chaine = []
        while v != source:
            u = chemin[v]
            flot_chaine = min(flot_chaine, residuel[u][v])
            arcs_chaine.append((u, v))
            v = u
        arcs_chaine.reverse()

        print(f"Chaîne améliorante trouvée : {arcs_chaine} avec flot = {flot_chaine}")

        # Mise à jour du graphe résiduel
        v = puits
        while v != source:
            u = chemin[v]
            residuel[u][v] -= flot_chaine
            residuel[v][u] += flot_chaine
            v = u

        afficher_matrice_residuelle(residuel)
        flot += flot_chaine

    return flot
