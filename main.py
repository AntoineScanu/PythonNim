import graphviz
from minimax import *
from tree import *

# Fonction pour jouer au jeu de Nim
def play_nim():
    # Initialisation des variables pour un jeu de Nim standard
    state = (1,2)
    player_turn = True  # Le joueur commence

    # Construction de l'arbre Minimax à partir de l'état initial
    root_node = MinimaxNode(state, True)
    build_minimax_tree(root_node)

    # Boucle principale du jeu
    while True:
        print("Etat actuel :", state)

        # Le joueur joue
        if player_turn:
            print("Tour du joueur.")
            pile = int(input("Choisissez une pile : ")) - 1
            remain = int(input("Choisissez le nombre d'éléments à enlever : "))
            state = state[:pile] + (state[pile] - remain,) + state[pile + 1 :]
            player_turn = False

        # L'ordinateur joue
        else:
            print("Tour de l'ordinateur.")
            score, new_state = best_move(state)
            pile = -1
            remain = -1
            for i, (a, b) in enumerate(zip(state, new_state)):
                if a != b:
                    pile = i
                    remain = a - b
            state = new_state
            print(f"L'ordinateur a enlevé {remain} élément(s) de la pile {pile+1}.")
            player_turn = True

        # Vérification de la fin de la partie
        if all(counters == 0 for counters in state):
            if not player_turn:
                print("L'ordinateur a gagné !")
            else:
                print("Le joueur a gagné !")

            # Création du graphe avec Graphviz
            graph = graphviz.Digraph(format='png')
            add_node_to_graph(graph, root_node)
            graph.render('minimax_tree')
            break

# Lancement du jeu
play_nim()