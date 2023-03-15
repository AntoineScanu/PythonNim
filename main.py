import graphviz
from minimax import *
from tree import *

# Fonction pour jouer au jeu de Nim
def nim():
    # Initialisation des variables pour un jeu de Nim standard
    etat = (1,2)
    tour_du_joueur = True  # Le joueur commence

    # Construction de l'arbre Minimax à partir de l'état initial
    root_node = MinimaxNode(etat, True)
    build_minimax_tree(root_node)

    # Boucle principale du jeu
    while True:
        print("Etat actuel :", etat)

        # Le joueur joue
        if tour_du_joueur:
            print("Tour du joueur.")
            pile = int(input("Choisissez une pile : ")) - 1
            restant = int(input("Choisissez le nombre d'éléments à enlever : "))
            etat = etat[:pile] + (etat[pile] - restant,) + etat[pile + 1 :]
            tour_du_joueur = False

        # L'ordinateur joue
        else:
            print("Tour de l'ordinateur.")
            score, nouvel_etat = best_move(etat)
            pile = -1
            restant = -1
            for i, (a, b) in enumerate(zip(etat, nouvel_etat)):
                if a != b:
                    pile = i
                    restant = a - b
            etat = nouvel_etat
            print(f"L'ordinateur a enlevé {restant} élément(s) de la pile {pile+1}.")
            tour_du_joueur = True

        # Vérification de la fin de la partie
        if all(allumettes == 0 for allumettes in etat):
            if not tour_du_joueur:
                print("L'ordinateur a gagné !")
            else:
                print("Le joueur a gagné !")
            # Création du graphe avec Graphviz
            graph = graphviz.Digraph(format='png')
            add_node_to_graph(graph, root_node)
            graph.render('minimax_tree')
            break
        
# Lancement du jeu
nim()