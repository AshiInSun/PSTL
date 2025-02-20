import random
from fractions import Fraction

def build_alias_table(PV):
    """
    Construit la table Alias à partir d'un vecteur de probabilités
    
    Args:
        PV (list): Liste des probabilités

    Returns:
        tuple: (prob_table, alias_table)
    """
    
    poor = []
    rich = []
    
    n_pv = len(PV)
    summ = sum(PV)
    ratio = n_pv / summ

    new_pv = [p * ratio for p in PV] 
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
        new_pv[tmp_rich] -= 1.0 - new_pv[tmp_poor]

        if new_pv[tmp_rich] < 1.0:
            poor.pop()
            rich.pop()
            poor.append(tmp_rich)

        else:
            poor.pop()

    return new_pv, alias    # Retourne les deux listes qu'on necessite pour le tirage de l'objet aleatoire 


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

# TESTS TEMPORAIRES
p1 = Fraction(1, 10) # 0.1
p2 = Fraction(2, 10) # 0.2
p3 = Fraction(7, 10) # 0.7
probs = [p1, p2, p3]  

print("Building alias table...")
new_pv, alias = build_alias_table(probs)

print("Sampling...")
samples = [sample_from_alias(new_pv, alias) for _ in range(10)]
print(samples)
