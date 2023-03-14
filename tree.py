import graphviz
from minimax import *

class MinimaxNode:
    def __init__(self, state, is_maximizing):
        # Stocker l'état du jeu associé à ce nœud
        self.state = state
        # Stocker le joueur associé à ce nœud (True pour maximiser, False pour minimiser)
        self.is_maximizing = is_maximizing
        # Stocker les nœuds enfants de ce nœud (initialisé à une liste vide)
        self.children = []
        # Stocker le score associé à ce nœud (initialisé à None)
        self.score = None
        
        self.isplayed=0



# Fonction récursive pour construire l'arbre Minimax
def build_minimax_tree(node):
    if node.score is not None:
        return

    for new_state in possible_new_states(node.state):
        child_node = MinimaxNode(new_state, not node.is_maximizing)
        node.children.append(child_node)
        build_minimax_tree(child_node)

    node.score = minimax(node.state, node.is_maximizing)

# Fonction récursive pour ajouter les nœuds à Graphviz
def add_node_to_graph(graph, node):
    label = f"{'Max' if node.is_maximizing else 'Min'}\n{node.score}"
    
    # Ajouter une couleur différente pour les nœuds représentant des positions perdantes
    color = 'red' if node.score == -1 else 'black'
    
    # Ajouter une étiquette supplémentaire pour indiquer si une position est gagnante ou perdante
    if node.score == -1:
        label += '\n(Perdant)'
    elif node.score == 1:
        label += '\n(Gagnant)'
    
    # Ajouter le noeud au graphe
    graph.node(str(id(node)), label=label, color=color)
    
    # Ajouter les noeuds fils récursivement
    for child in node.children:
        add_node_to_graph(graph, child)
        
        # Ajouter l'arc entre le noeud parent et le noeud fils
        graph.edge(str(id(node)), str(id(child)))
