import random


# j'ai séparé en deux fonction le pseudo-code que tu m'as donné, le resultat devrait etre le meme

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

    new_pv = [p * ratio for p in PV]    # IG c'est ici que t'as oublier de d'appliquer ratio
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
        tmp_poor = poor.pop()
        tmp_rich = rich.pop()

        alias[tmp_poor] = tmp_rich
        new_pv[tmp_rich] -= 1.0 - new_pv[tmp_poor]

        if new_pv[tmp_rich] < 1.0:      # IG c'est tmp_rich a la place de tmp_pv, t'as mis
            poor.append(tmp_rich)
        else:
            rich.append(tmp_rich)

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

    return i if i <= new_pv[i] else alias[i]


# Test marche pas , A REVOIR
probs = [0.1, 0.2, 0.7]  
new_pv, alias = build_alias_table(probs)

samples = [sample_from_alias(new_pv, alias) for _ in range(10)]
print(samples)
