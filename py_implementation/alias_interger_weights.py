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
    
    # Temporaire, utiliser pour les tests avec distributions aleatoire, comme on veut uniquement voir ceux ou l'on rentre dans les conditions
    temp_bool = False

    # Preconditions sur les Inputs
    if not objects or not weights:
        raise ValueError("Les listes 'objects' et 'weights' ne peuvent pas etre vides")
    
    if len(objects) != len(weights):
        raise ValueError("Les listes 'objects' et 'weights' doivent etre de meme taille")
    
    if any(w <= 0 for w in weights):
        raise ValueError("Les poids doivent etre des entiers strictement positifs")


    n = len(objects)
    total_weight = sum(weights)
    cell_size = total_weight // n
    rest = total_weight % cell_size

    # Etend les listes SI la somme des poids n'est pas divisble par n
    if rest > 0:
        objects.append("xn")
        weights.append(cell_size - rest)
        total_weight += weights[-1]
    
    m = total_weight // cell_size
    table = [None] * m
    heavy_stack = [i for i, w in enumerate(weights) if w >= cell_size]
    light_stack = [i for i, w in enumerate(weights) if w < cell_size]
    k = 0

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
    
    if k == m - 2:

        temp_bool = True


        print("------------------------------------------ CONDITION (k == m - 2) -----------------------------------------")
        i = light_stack.pop()
        light_obj, light_weight = objects[i], weights[i]
        j = light_stack.pop()
        light_obj2, light_weight2 = objects[j], weights[j]
        table[k] = (light_weight2, light_obj2, light_obj)

    elif k == m-1 and table[m-1] == None:

        temp_bool = True


        print("------------------------------- CONDITION ( k == m-1 and table[m-1] == None) --------------------------------")
        i = light_stack.pop()
        light_obj, light_weight = objects[i], weights[i]
        j = light_stack.pop()
        light_obj2, light_weight2 = objects[j], weights[j]
        if light_obj == "xn":
            table[k] = (light_weight2, light_obj2, light_obj)
        else:
            table[k] = (light_weight, light_obj, light_obj2)
         
    return table, cell_size, temp_bool


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
    
    while True:
        size = len(table)
        index = random.randint(0, size - 1)
        weight, obj1, obj2 = table[index]
        result = obj1 if random.randint(1, cs) <= weight else obj2

        if result != "xn":
            return result
