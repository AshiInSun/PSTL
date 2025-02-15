import random

def unuran_table_building(weights):
    """
    Construit une table Alias basée sur des poids entiers pour générer des variables aléatoires.
    
    Inputs:
        objects (list): Liste des objets qu'on souhaite generer aleatoirement
        weights (list): Liste des poids entiers associés aux objets
    
    Outputs:
        list: Une table de triplets (w, x, x'), utilisée pour la génération 
    """
    
    # Temporaire, utiliser pour les tests avec distributions aleatoire, comme on veut uniquement voir ceux ou l'on rentre dans les conditions
    temp_bool = False


    n = len(weights)

    total_weight = sum(weights)
    cell_size = n / total_weight # Notons que dans notre algo nous faisons total_weight//n
    
    m = total_weight // cell_size + 1
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
