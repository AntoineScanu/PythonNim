from minimaxAB import best_move
from anytree import Node, RenderTree

# Définition d'une fonction récursive pour créer l'arbre de décision
def build_tree(state, node, depth, max_depth):
    if depth == max_depth:
        return

    # Calcul des coups possibles pour l'ordinateur
    for pile in range(len(state)):
        for remain in range(1, state[pile] + 1):
            new_state = state[:pile] + (state[pile] - remain,) + state[pile + 1 :]
            score, _ = best_move(new_state)

            # Ajout d'un noeud pour chaque coup possible
            child = Node(f"L'ordinateur enlève {remain} éléments de la pile {pile+1}. Score : {score}", parent=node, state=new_state)
            
            # Construction de l'arbre à partir des noeuds fils
            build_tree(new_state, child, depth+1, max_depth)

# Initialisation des variables pour un jeu de Nim standard à 3 piles
state = (3, 4, 5)

# Création de la racine de l'arbre de décision
root = Node(f"Etat initial : {state}", state=state)

# Construction de l'arbre de décision
build_tree(state, root, 0, 3)

# Affichage de l'arbre de décision
for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")
