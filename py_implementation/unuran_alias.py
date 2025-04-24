import random
from collections import Counter
from fractions import Fraction

def build_alias_table(PV):
    """
    Construit la table Alias à partir d'un vecteur de probabilités
    
    Args:
        PV (list): Liste des probabilités

    Returns:
        tuple: (prob_table, alias_table)
    """

    # PRECONDITIONS
    if not PV:
        raise ValueError("La liste de probabilité ne peut pas etre vide")
    
    if any(p < 0 for p in PV):
        raise ValueError("Les probabilités ne peuvent pas etre negatives")
    
    poor = []
    rich = []
    
    n_pv = len(PV)
    summ = sum(PV)
    ratio = Fraction(n_pv, summ)

    new_pv = [Fraction(p) * ratio for p in PV] 
    alias = [None] * n_pv

    for i in range(n_pv):
        if new_pv[i] >= 1.0:
            rich.append(i)
            alias[i] = i  
        else:
            poor.append(i)
            #i.e alias[i] = None 

    # Algorithme "Robin Hood" (Marsaglia)
    while poor:
        tmp_poor = poor[-1]
        tmp_rich = rich[-1]

        alias[tmp_poor] = tmp_rich
        new_pv[tmp_rich] -= Fraction(1.0) - new_pv[tmp_poor]

        if new_pv[tmp_rich] < 1.0:
            poor.pop()
            rich.pop()
            poor.append(tmp_rich)

        else:
            poor.pop()

    return [float(p) for p in new_pv], alias    # Retourne les deux listes qu'on necessite pour le tirage de l'objet aleatoire 


def sample_from_alias(new_pv, alias):
    """
    Genere un nombre aléatoire selon la distribution Alias construite

    Args:
        new_pv (list): Liste des probabilités ajustées
        alias (list): Table d'alias 

    Returns:
        int: Index de l'élément généré
    """
    n_pv = len(new_pv)
    i = random.randint(0, n_pv - 1)  

    return i if random.random() <= new_pv[i] else alias[i]
