import graphviz             # Importation de la bibliothèque graphviz pour créer un graphe

# Fonction pour jouer au jeu de Nim
def nim():
    # Initialisation des variables pour un jeu de Nim standard
    etat = (3,3)             # L'état initial est un ensemble de plusieurs élement, le chiffre est le nombre d'allumettes dans chaque pile
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
            add_node_to_graph(graph, root_node,True)
            graph.render('minimax_tree')
            
            break        
# Lancement du jeu

def minimax(etat, est_max, alpha=-1, beta=1):
    # Vérifier si le jeu est terminé et renvoyer le score s'il l'est
    if (score := evaluer(etat, est_max)) is not None:
        return score
    scores = []
    # Générer tous les nouveaux états possibles pour l'état actuel
    for nouvel_etat in possible_nouvel_etats(etat):
        # Récursivement, évaluer tous les états possibles en alternant entre minimiser et maximiser
        # Ajouter chaque score obtenu à la liste scores
        scores.append(score := minimax(nouvel_etat, not est_max, alpha, beta))
        # Mettre à jour alpha ou beta selon le cas
        if est_max:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)
            
        # Vérifier si la coupe alpha-beta peut être effectuée
        if beta <= alpha:
            break
    # Choisir le meilleur score en fonction du joueur actuel (maximiser ou minimiser)
    return (max if est_max else min)(scores)

def evaluer(etat, est_max):
    # Vérifier si tous les compteurs sont égaux à 0, ce qui signifie que le jeu est terminé
    if all(allumettes == 0 for allumettes in etat):
        # Si le joueur actuel est le joueur qui cherche à maximiser le score, il a gagné
        # Sinon, c'est l'autre joueur qui a gagné
        return 1 if est_max else -1
    
    # Vérifier si toutes les positions suivantes sont perdantes pour l'adversaire
    for nouvel_etat in possible_nouvel_etats(etat):
        if evaluer(nouvel_etat, not est_max) != -1:
            return None
    
    # Si toutes les positions suivantes sont perdantes pour l'adversaire, cette position est perdante pour le joueur actuel
    return -1

def possible_nouvel_etats(etat):
    # Parcourir chaque pile dans l'état actuel
    for pile, allumettes in enumerate(etat):
        # Parcourir chaque valeur possible de compteurs restants pour cette pile
        for restant in range(allumettes):
            # Générer un nouvel état en retirant le nombre de compteurs spécifié de cette pile
            # et en ajoutant un nouveau compteur avec la valeur restante
            yield etat[:pile] + (restant,) + etat[pile + 1 :]
            
def meilleur_coup(etat):
    return max(
        ((score := minimax(nouvel_etat, est_max=False)), nouvel_etat)
        for nouvel_etat in possible_nouvel_etats(etat)
    )
    
    

class MinimaxNode:
    def __init__(self, etat, est_max):
        # Stocker l'état du jeu associé à ce nœud
        self.etat = etat
        # Stocker le joueur associé à ce nœud (True pour maximiser, False pour minimiser)
        self.est_max = est_max
        # Stocker les nœuds enfants de ce nœud (initialisé à une liste vide)
        self.children = []
        # Stocker le score associé à ce nœud (initialisé à None)
        self.score = None
        
        self.isplayed=0

# Fonction récursive pour construire l'arbre Minimax
def build_minimax_tree(node):
    """Construit récursivement l'arbre Minimax à partir du nœud racine."""
    # Évalue le score de l'état actuel
    node.score = evaluer(node.etat,False)
    # Si l'état actuel est un état final, on arrête la construction de l'arbre
    if node.score is not None:
        return
    # Pour chaque nouvel état possible à partir de l'état actuel
    for nouvel_etat in possible_nouvel_etats(node.etat):
        # Créer un nœud enfant avec le nouvel état
        enfant_node = MinimaxNode(nouvel_etat, not node.est_max)
        # Évalue le score du nœud enfant avec l'algorithme Minimax
        enfant_node.score = minimax(nouvel_etat, enfant_node.est_max)
        # Construit récursivement l'arbre Minimax à partir du nœud enfant
        build_minimax_tree(enfant_node)
        # Ajoute le nœud enfant à la liste des enfants du nœud actuel
        node.children.append(enfant_node)
        # Crée un graphe Graphviz pour visualiser l'arbre Minimax
    graph = graphviz.Digraph(format='png')
    # Ajoute le nœud actuel au graphe avec sa couleur correspondant au joueur en cours
    add_node_to_graph(graph, node, node.est_max)

# Fonction récursive pour ajouter les nœuds à Graphviz
def add_node_to_graph(graph, node, est_max, parent_node=None):
    """Ajoute un nœud à un graphe Graphviz et récursivement tous ses enfants."""
    label = f"{node.etat}\n({node.score})"
    if est_max:
        shape = 'box'
    else:
        shape = 'oval'
    # Ajout du noeud au graphe
    graph.node(str(id(node)), label=label, shape=shape)
    # Ajout d'un lien entre le noeud et son parent s'il existe
    if parent_node is not None:
        graph.edge(str(id(parent_node)), str(id(node)))
    # Ajout des enfants du noeud actuel
    for child_node in node.children:
        add_node_to_graph(graph, child_node, not est_max, node)

nim()