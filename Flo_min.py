from affichage import afficher_matrice

def construire_graphe_residuel(capacites: list, couts: list, flots: list):
    n = len(capacites)
    capacites_resid = [[0] * n for _ in range(n)]
    couts_resid = [[float('inf')] * n for _ in range(n)]

    for u in range(n):
        for v in range(n):
            if capacites[u][v] > 0:
                # Calculer les capacités résiduelles
                capacites_resid[u][v] = capacites[u][v] - flots[u][v]
                if capacites_resid[u][v] > 0:
                    couts_resid[u][v] = couts[u][v]  # Coût direct

                # Ajouter les capacités et coûts inverses
                capacites_resid[v][u] = flots[u][v]
                if capacites_resid[v][u] > 0:
                    couts_resid[v][u] = -couts[u][v]  # Coût inverse

    return capacites_resid, couts_resid

def trouver_plus_court_chemin_bellman_ford(source: int, puits: int, capacites_resid: list, couts_resid: list):
    n = len(capacites_resid)
    distances = [float('inf')] * n
    parents = [-1] * n
    distances[source] = 0

    # Appliquer l'algorithme Bellman-Ford
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if capacites_resid[u][v] > 0 and distances[u] + couts_resid[u][v] < distances[v]:
                    distances[v] = distances[u] + couts_resid[u][v]
                    parents[v] = u

    # Pas de chemin vers le puits
    if distances[puits] == float('inf'):
        return None, None

    # Reconstituer le chemin à partir des parents
    chemin = []
    actuel = puits
    while actuel != -1:
        chemin.insert(0, actuel)
        actuel = parents[actuel]

    return chemin, distances[puits]

def calculer_flot_minimal_cout(flot: dict, flot_vise, source=0, puits=None):
    n = flot["n"]
    if puits is None:
        puits = n - 1

    capacites = flot["capacites"]
    couts = flot["couts"]
    flots_actuels = [[0] * n for _ in range(n)]
    flot_envoye = 0

    capacites_resid, couts_resid = construire_graphe_residuel(capacites, couts, flots_actuels)

    cout_final = 0

    while  flot_envoye < flot_vise:
        chemin, cout_chemin = trouver_plus_court_chemin_bellman_ford(source, puits, capacites_resid, couts_resid)
        if chemin is None:
            break  # Aucun chemin supplémentaire possible

        # Trouve combien de flots on va envoyer
        capacite_min = float('inf')
        for i in range(len(chemin) - 1):
            u = chemin[i]
            v = chemin[i + 1]
            capacite_min = min(capacite_min, capacites_resid[u][v])

        augmentation = min(capacite_min, flot_vise - flot_envoye)

        for i in range(len(chemin) - 1):
            u = chemin[i]
            v = chemin[i + 1]
            flots_actuels[u][v] += augmentation
            flots_actuels[v][u] -= augmentation

        flot_envoye += augmentation
        cout_final += cout_chemin * augmentation
        capacites_resid, couts_resid = construire_graphe_residuel(capacites, couts, flots_actuels)
        afficher_matrice(capacites_resid, "Capacités résiduelles après mise à jour")
        afficher_matrice(couts_resid, "Coûts résiduels après mise à jour")

    return flot_envoye, cout_final

