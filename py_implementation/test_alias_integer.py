from collections import Counter
from alias_interger_weights import *

def test():
    
    test_cases = [
        # Valide
        (["A", "B", "C"], [3, 4, 5], "Cas simple avec 3 objets"),

        # Donne une table alias differente au test precedent bien que meme poids. Est ce un probleme? Veut on toujours la meme table 
        (["A", "C", "B"], [3, 5, 4], "Cas simple avec 3 objets, ordre des poids different"),

        # On ne veut pas que m'objet virtuel soit tiré, comment gerer ca?
        (["A", "B", "C"], [3, 4, 6], "Cas où un élément virtuel est ajouté"),        

        # Tests à ajouter
    ]
    for objects, weights, description in test_cases:
        print(f"Test: {description}")

        try:
            print(f"    Liste des objet et leur poids: {dict(zip(objects, weights))}")
            print("    - Construction de la table Alias...")
            alias_table, cell_size = table_building(objects, weights)
            print(f"      Table Alias construite: {alias_table}")

            # Vérification de la génération aléatoire
            if alias_table:  
                print("    - Generation de 100 tirages aleatoires...")
                samples = [generation(alias_table, cell_size) for _ in range(1000)]
                print(f"      Echantillons générés: {dict(Counter(samples))}")
            print()
        
        except Exception as e:
            print(f"ERREUR: {e}")
            break

if __name__ == "__main__":
    test()