import graphviz             # Importation de la bibliothèque graphviz pour créer un graphe
from minimax import *       # Importation des fonctions de l'algorithme Minimax
from tree import *          # Importation de la classe MinimaxNode pour représenter les noeuds de l'arbre Minimax

# Fonction pour jouer au jeu de Nim
def nim():
    # Initialisation des variables pour un jeu de Nim standard
    etat = (1,2)             # L'état initial est un ensemble de plusieurs élement, le chiffre est le nombre d'allumettes dans chaque pile
    tour_du_joueur = True    # La variable tour_du_joueur est un booléen qui indique si c'est le tour du joueur ou non

    # Construction de l'arbre Minimax à partir de l'état initial
    root_node = MinimaxNode(etat, True)    # Création du noeud racine de l'arbre avec l'état initial et le joueur qui doit jouer
    build_minimax_tree(root_node)          # Construction de l'arbre Minimax en ajoutant des noeuds à partir du noeud racine

    # Boucle principale du jeu
    while True:
        print("Etat actuel :", etat)

        # Le joueur joue
        if tour_du_joueur:
            print("Tour du joueur.")
            pile = int(input("Choisissez une pile : ")) - 1      # Le joueur choisit la pile à modifier en entrant un nombre
            restant = int(input("Choisissez le nombre d'éléments à enlever : "))  # Le joueur choisit le nombre d'allumettes à enlever en entrant un nombre
            etat = etat[:pile] + (etat[pile] - restant,) + etat[pile + 1 :]  # Modification de l'état du jeu en enlevant le nombre d'allumettes choisi dans la pile choisie
            tour_du_joueur = False   # Le tour du joueur est terminé, c'est au tour de l'ordinateur
    
        # L'ordinateur joue
        else:
            print("Tour de l'ordinateur.")
            score, nouvel_etat = meilleur_coup(etat)    # L'ordinateur choisit le meilleur coup à jouer en utilisant l'algorithme Minimax et obtient le score et le nouvel état du jeu
            pile = -1
            restant = -1
            for i, (a, b) in enumerate(zip(etat, nouvel_etat)):
                if a != b:
                    pile = i
                    restant = a - b
            etat = nouvel_etat   # Modification de l'état du jeu avec le nouvel état calculé par l'ordinateur
            print(f"L'ordinateur a enlevé {restant} élément(s) de la pile {pile+1}.")  # Affichage du coup joué par l'ordinateur
            tour_du_joueur = True   # Le tour de l'ordinateur est terminé, c'est au tour du joueur

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