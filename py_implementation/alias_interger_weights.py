def table_building(objects, weights):

    n = len(objects)
    total_weight = sum(weights)
    cell_size = total_weight // n
    rest = total_weight % n

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
                table[m-1] = (light_weight, light_obj, heavy_obj)
            
            weights[i] -= light_weight

        else:
            table[k] = (cell_size, heavy_obj, None)
            weights[i] -= cell_size

        if 0 < weights[i] < cell_size:
                light_stack.append(i)               
        elif weights[i] >= cell_size:
            heavy_stack.append(i)  
        k += 1
    
    if k == m - 2:
        i = light_stack.pop()
        light_obj, light_weight = objects[i], weights[i]
        j = light_stack.pop()
        light_obj2, light_weight2 = objects[j], weights[j]
        table[k] = (light_weight2, light_obj2, light_obj)

    elif k == m-1 and table[m-1] == None:
        i = light_stack.pop()
        light_obj, light_weight = objects[i], weights[i]
        j = light_stack.pop()
        light_obj2, light_weight2 = objects[j], weights[j]
        if light_obj == "xn":
            table[k] = (light_weight2, light_obj2, light_obj)
        else:
            table[k] = (light_weight, light_obj, light_obj2)
            
    
    return table


def sample_from_alias_table(alias_table):
    """
    Génère un objet aléatoire à partir de la table Alias construite.
    
    Args:
        alias_table (list): Table de triplets (v, x, x').
    
    Returns:
        str: L'objet généré aléatoirement.
    """
    import random
    index = random.randint(0, len(alias_table) - 1)
    weight, obj, alias_obj = alias_table[index]
    return obj if random.randint(1, weight) == 1 else alias_obj


# Exemple d'utilisation
objects = ['A', 'B', 'C']
weights = [3, 7, 5]
alias_table = table_building(objects, weights)
print(f"Table Alias: {alias_table}")

for _ in range(5):
    print(f"Échantillon généré: {sample_from_alias_table(alias_table)}")
