import random

def table_building(objects, weights):
    """
    Construit une table Alias basée sur des poids entiers pour générer des variables aléatoires.
    
    Inputs:
        objects (list): Liste des objets qu'on souhaite generer aleatoirement
        weights (list): Liste des poids entiers associés aux objets
    
    Outputs:
        list: Une table de triplets (w, x, x'), utilisée pour la génération 

    Raises:
        ValueError: Si les listes sont vides, de tailles différentes ou contiennent des poids non strictement positif
    """

    # PRECONDITIONS
    if not objects or not weights:
        raise ValueError("Les listes 'objects' et 'weights' ne peuvent pas etre vides")
    
    if len(objects) != len(weights):
        raise ValueError("Les listes 'objects' et 'weights' doivent etre de meme taille")
    
    if any(w <= 0 for w in weights):
        raise ValueError("Les poids doivent etre des entiers strictement positifs")

    # INITIALISATIONS
    n = len(objects)
    total_weight = sum(weights)
    cell_size = total_weight // n
    rest = total_weight % n
    r = total_weight % cell_size

    if r > 0:    # Etend les listes SI la somme des poids n'est pas divisble par n
        objects.append("xn")
        weights.append(cell_size - r)
        total_weight += weights[-1]
    
    m = total_weight // cell_size
    table = [None] * m
    heavy_stack = [i for i, w in enumerate(weights) if w >= cell_size]
    light_stack = [i for i, w in enumerate(weights) if w < cell_size]
    k = 0

    # TODO INVARIANT
    index_invariant = 0 
    def check_invariant():
        nonlocal index_invariant

        assert True, f"Invariant {index_invariant} fail: ..." # Temporairement à True 
        index_invariant += 1

    check_invariant()   # verification avant boucle

    # ALGORITHME
    while heavy_stack:

        i = heavy_stack.pop()
        heavy_obj, heavy_weight = objects[i], weights[i]

        if light_stack:
            j = light_stack.pop()
            light_obj, light_weight = objects[j], weights[j]

            if light_obj != "xn":
                table[k] = (light_weight, light_obj, heavy_obj)
            else:
                table[m-1] = (cell_size - light_weight, heavy_obj, light_obj)
                k -= 1
            
            weights[i] -= (cell_size-light_weight)

        else:
            table[k] = (cell_size, heavy_obj, None)
            weights[i] -= cell_size

        if 0 < weights[i] < cell_size:
                light_stack.append(i)               
        elif weights[i] >= cell_size:
            heavy_stack.append(i)  
        k += 1
        
        check_invariant()   # verification fin boucle
    return table, cell_size


def generation(table, cs):
    """
    Génère un objet aléatoire à partir de la table Alias
    L'objet virtuel de la table d'alias ( xn ) ne peut pas etre retourner 
    
    Inputs:
        table (list): La table de triplets (v, x, x')
        cs (int): La moyenne des poids des objets
    
    Output:
        str: L'objet généré aléatoirement
    """
    
    size = len(table)
    total_weight = size * cs
    
    # Vérifier si l'objet virtuel existe
    last_weight, _, potential_xn = table[-1]
    
    if potential_xn == "xn":
        xn_weight = cs - last_weight
        total_weight -= xn_weight  # Permet d'éviter de generer l'objet virtuel
    
    
    rand_value = random.randint(0, total_weight - 1)

    index = rand_value // cs
    weight, obj1, obj2 = table[index]

    return obj1 if (rand_value % cs) < weight else obj2


