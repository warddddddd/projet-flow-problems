from affichage import lire_fichier_flots, afficher_matrices
from Flo_Max import ford_fulkerson
from poussé_ééti import pousser_reetiqueter
from Flo_min import calculer_flot_minimal_cout 
from complexity import analyze_complexity, plot_results_by_graph_size

def main():
    
    
    try:
         # Propose à l'utilisateur de choisir une action
        choix_principal = input("Choisissez une action : (1) Exécuter un algorithme (2) Analyser la complexité : ")

        if choix_principal == "1":
        # Demande à l'utilisateur le numéro du problème (ex: "1" pour lire "1.txt")
            numero_probleme = input("Veuillez entrer le numéro du problème (exemple : 1 pour 1.txt) : ")
            
            # Construit le nom du fichier à partir du numéro du problème
            nom_fichier = f"{numero_probleme}.txt"
            
            # Lit le fichier et récupère le nombre de sommets, la matrice des capacités et éventuellement la matrice des coûts
            n, capacites, couts = lire_fichier_flots(nom_fichier)
            
            # Affiche le nombre de sommets lu
            print(f"Nombre de sommets : {n}")
            
            # Affiche la (les) matrice(s) lue(s) (capacités et, si disponible, coûts)
            afficher_matrices(capacites=capacites, couts=couts)
            
            # Demande à l'utilisateur de saisir l'indice du sommet source
            source = int(input("Entrez l'indice du sommet source (0-indexé) : "))
            
            # Demande à l'utilisateur de saisir l'indice du sommet puits
            puits = int(input("Entrez l'indice du sommet puits (0-indexé) : "))

            # Si une matrice de coûts est disponible, on propose les 4 algorithmes, sinon seulement les 2 premiers
            if couts is not None:
                # Propose un choix d'algorithmes : 
                # 1) Ford-Fulkerson (flot max)
                # 2) Pousser-Réétiqueter (Push-Relabel) (flot max)
                # 3) Flot de coût minimal pour flot max
                # 4) Flot de coût minimal pour un flot cible
                choix_algo = input("Choisissez l'algorithme : (1) Ford-Fulkerson (2) Pousser-Réétiqueter (3) Flot max de coût minimal (4) Flot de coût minimal pour un flot cible : ")
            else:
                # Si pas de matrice de coûts, on ne propose que les algorithmes de flot max sans coût
                choix_algo = input("Choisissez l'algorithme : (1) Ford-Fulkerson (2) Pousser-Réétiqueter : ")

            # Si l'utilisateur choisit "1"
            if choix_algo == "1":
                # Lance Ford-Fulkerson sur les données
                flot_max = ford_fulkerson(capacites, source, puits)
                # Affiche le résultat
                print(f"Flot maximal avec Ford-Fulkerson : {flot_max}")
            
            # Si l'utilisateur choisit "2"
            elif choix_algo == "2":
                # Lance l'algorithme Pousser-Réétiqueter (Push-Relabel) sur les données
                flot_max = pousser_reetiqueter(capacites, source, puits)
                # Affiche le résultat
                print(f"Flot maximal avec Pousser-Réétiqueter : {flot_max}")
            
            # Si l'utilisateur choisit "3" et que les coûts sont disponibles
            elif choix_algo == "3" and couts is not None:
                # Lance le calcul du flot de coût minimal (sans flot puits, on maximise simplement le flot)
                flot_max, cout_total = calculer_flot_minimal_cout(
                    {"n": n, "capacites": capacites, "couts": couts}, 
                    flot_vise=float('inf'),
                    source=source,
                    puits=puits
                )
                
                # Affiche le résultat
                print(f"Flot maximal avec coût minimal : {flot_max}, coût total : {cout_total}")
                
                      # Si l'utilisateur choisit "4" et que les coûts sont disponibles
            elif choix_algo == "4" and couts is not None:
                # Demande le flot cible que l'on souhaite atteindre
                flot_vise = int(input("Entrez la valeur de flot cible : "))
                # Lance le calcul du flot de coût minimal pour atteindre ce flot cible
                flot_atteint, cout_total = calculer_flot_minimal_cout(
                    {"n": n, "capacites": capacites, "couts": couts},
                    flot_vise=flot_vise,
                    source=source,
                    puits=puits
                )
                # Affiche le résultat
                print(f"Flot atteint : {flot_atteint}, coût total : {cout_total}")      
                
                
            else:
                # Si l'utilisateur fait un choix invalide (ex: algorithme 3 ou 4 sans coûts) ou autre
                print("Choix invalide ou matrice de coûts non disponible.")
            
                
        elif choix_principal == "2":
            print("Début de l'analyse de complexité...")
            n_values = [10, 20, 40, 100, 1000]
            results = analyze_complexity()  # Run the analysis and get results
            plot_results_by_graph_size(results, n_values)
            print("Analyse de complexité terminée.")

        else:
            print("Choix invalide. Veuillez entrer '1', '2' ou 'q'.")
              
                

    except FileNotFoundError:
        # Si le fichier spécifié n'est pas trouvé, on affiche un message d'erreur
        print("Erreur : Le fichier spécifié est introuvable.")
    except ValueError as e:
        # Si une erreur de valeur (par exemple un problème de format dans le fichier) est détectée
        print(f"Erreur : {e}")
        

# Point d'entrée du script : si ce fichier est exécuté directement, on lance main()
if __name__ == "__main__":
    main()

