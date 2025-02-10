from collections import Counter
from alias_interger_weights import *

def test():
    
    test_cases = [
        
        # NEED FIX: Si liste vide, division par 0, Erreurs, problemes
        #([], [], "Cas listes vides"),

        # Valide
        (["A", "B", "C"], [3, 4, 5], "Cas simple avec 3 objets"),

        # Donne une table alias differente au test precedent bien que meme poids. Est ce un probleme? Veut on toujours la meme table 
        (["A", "C", "B"], [3, 5, 4], "Cas simple avec 3 objets, ordre des poids different"),

        # Valide
        (["A", "B", "C"], [3, 4, 6], "Cas où un élément virtuel est ajouté"),  

        # NEED FIX: L'objet avec le poid vide est mit dans la table alias, inutile
        (["A", "B", "C", "D"], [3, 4, 5, 0], "Cas objet avec poids 0")         
        
        # Tests à ajouter
    ]
    for objects, weights, description in test_cases:
        print(f"Test: {description}")

        try:
            print(f"    Liste des objet et leur poids: {dict(zip(objects, weights))}")
            print("    - Construction de la table Alias...")
            alias_table, cell_size, _ = table_building(objects, weights)
            print(f"      Table Alias construite: {alias_table}")

            # Vérification de la génération aléatoire
            if alias_table:  
                print("    - Generation de 1000 tirages aleatoires...")
                samples = [generation(alias_table, cell_size) for _ in range(1000)]
                print(f"      Echantillons générés: {dict(Counter(samples))}")
            print()
        
        except Exception as e:
            print(f"ERREUR: {e}")
            break

def test_random_distributions(num_tests=10, num_samples=1000):

    print("Génération de tests avec distribution aléatoire...")

    for index_test in range(1, num_tests + 1):

        try:
            num_objects = random.randint(3, 10)
            objects = [f"o{i}" for i in range(1, num_objects + 1)]
            weights = [random.randint(1, 1000000000) for _ in range(num_objects)]  # Poids entre 1 et 10
            
            alias_table, cs, cond_bool = table_building(objects, weights)

            # On passe au suivant si on est pas rentrer dans une des deux conditions
            if not(cond_bool):  
                continue

            print(f"Test {index_test}:")

            print(f"    Liste des objet et leur poids: {dict(zip(objects, weights))}")

            print(f"    Table Alias construite: {alias_table}")
            print(f"    Cell size: {cs}")

            if alias_table:  
                    generated = Counter(generation(alias_table, cs) for _ in range(num_samples))

                    print(f"    Fréquences des objets générés (sur {num_samples} essais):")
                    for obj, count in generated.items():
                        print(f"        - {obj}: {count / num_samples:.2f} ({count} fois)")
            print("\n")

        except Exception as e:
            print(f"ERREUR: {e}")
            break

if __name__ == "__main__":
    #test()
    test_random_distributions(10000000)
