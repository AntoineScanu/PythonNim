
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