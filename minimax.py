
def minimax(state, is_maximizing, alpha=-1, beta=1):
    # Vérifier si le jeu est terminé et renvoyer le score s'il l'est
    if (score := evaluate(state, is_maximizing)) is not None:
        return score
    scores = []
    # Générer tous les nouveaux états possibles pour l'état actuel
    for new_state in possible_new_states(state):
        # Récursivement, évaluer tous les états possibles en alternant entre minimiser et maximiser
        # Ajouter chaque score obtenu à la liste scores
        scores.append(score := minimax(new_state, not is_maximizing, alpha, beta))
        # Mettre à jour alpha ou beta selon le cas
        if is_maximizing:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)
            
        # Vérifier si la coupe alpha-beta peut être effectuée
        if beta <= alpha:
            break
    # Choisir le meilleur score en fonction du joueur actuel (maximiser ou minimiser)
    return (max if is_maximizing else min)(scores)

def evaluate(state, is_maximizing):
    # Vérifier si tous les compteurs sont égaux à 0, ce qui signifie que le jeu est terminé
    if all(counters == 0 for counters in state):
        # Si le joueur actuel est le joueur qui cherche à maximiser le score, il a gagné
        # Sinon, c'est l'autre joueur qui a gagné
        return 1 if is_maximizing else -1
    
    # Vérifier si toutes les positions suivantes sont perdantes pour l'adversaire
    for new_state in possible_new_states(state):
        if evaluate(new_state, not is_maximizing) != -1:
            return None
    
    # Si toutes les positions suivantes sont perdantes pour l'adversaire, cette position est perdante pour le joueur actuel
    return -1

def possible_new_states(state):
    # Parcourir chaque pile dans l'état actuel
    for pile, counters in enumerate(state):
        # Parcourir chaque valeur possible de compteurs restants pour cette pile
        for remain in range(counters):
            # Générer un nouvel état en retirant le nombre de compteurs spécifié de cette pile
            # et en ajoutant un nouveau compteur avec la valeur restante
            yield state[:pile] + (remain,) + state[pile + 1 :]
            
def best_move(state):
    return max(
        ((score := minimax(new_state, is_maximizing=False)), new_state)
        for new_state in possible_new_states(state)
    )