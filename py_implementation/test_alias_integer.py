import sys
from collections import Counter
from alias_interger_weights import *

MAX_OBJECTS = 10                # Nombre maximum d'objets générés
MAX_WEIGHT = 100                # Poids maximum pour un objet
DEFAULT_TEST_AMOUNT = 100       # Nombre de tests par défaut
DEFAULT_SAMPLES = 1000          # Nombre d’échantillons générés par test
DEFAULT_TOLERANCE = 0.1         # Seuil de tolérance pour la vérification des distributions, par défaut à 1 car le comportement par défaut ne genere que 1 sample


def manual_tests():
    
    test_cases = [
        
        # Erreur
        #([], [], "Cas listes vides"),

        # Erreur
        #(["A"], [1, 2], "Cas tailles des listes differents"),

        # Warning, on devrait filtrer (enlever) les poids à 0 selon le papier 
        (["A", "B", "C"], [0, 1, 2], "Cas poids à 0"),

        # Erreur
        #(["A", "B", "C"], [-1, 1, 2], "Cas poids negatif"),

        # Valide
        (["A", "B", "C"], [3, 4, 5], "Cas simple avec 3 objets"),

        # Donne une table alias differente au test precedent bien que meme poids.
        (["A", "C", "B"], [3, 5, 4], "Cas simple avec 3 objets, ordre des poids different"),

        # Valide
        (["A", "B", "C"], [3, 4, 6], "Cas où un élément virtuel est ajouté"),  

        # Valide
        (["A", "B", "C", "D"], [1, 1, 1, 7], "Cas où un élément lourd est divisé en deux")       
        
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
                print("    - Generation de 1000 tirages aleatoires...")
                samples = [generation(alias_table, cell_size) for _ in range(1000)]
                print(f"      Echantillons générés: {dict(Counter(samples))}")
            print()
        
        except Exception as e:
            print(f"ERREUR: {e}")
            break

def random_distributions_tests(num_tests=DEFAULT_TEST_AMOUNT, num_samples=DEFAULT_SAMPLES,
                                seuil_tolerance=DEFAULT_TOLERANCE, printer=False):

    print("Génération de tests avec distribution aléatoire...")


    # Renvoi True quand un problème est détecté, pour activer l'affichage
    def check_frequencies(objects, weights, generated):
        total_weight = sum(weights)
        expected_frequencies = {obj: w / total_weight for obj, w in zip(objects, weights)}
        observed_frequencies = {obj: generated.get(obj, 0) / num_samples for obj in objects}

        for obj in objects:
            if abs(expected_frequencies[obj] - observed_frequencies[obj]) > seuil_tolerance:
                return True     # Problème détecté, affichage activé

        return False

    # Renvoi True quand un problème est détecté, pour activer l'affichage
    def check_last_cells(alias_table):
        if alias_table[-1][2] is None:
            return False    # Hypothèse respectée, pas besoin d'afficher
        
        # Cas où l'élément virtuel est dans la dernière case
        if alias_table[-1][2] == "xn":  
            if alias_table[-2][2] is None:
                return False    # Hypothèse respectée
            return True     # Problème détecté, on active l'affichage

        return True     # Problème détecté

    for index_test in range(1, num_tests + 1):
        
        try:
            # Objets et poids associés aleatoires
            num_objects = random.randint(3, MAX_OBJECTS)
            objects = [f"o{i}" for i in range(1, num_objects + 1)]
            weights = [random.randint(1, MAX_WEIGHT) for _ in range(num_objects)]
            
            # Creation de la table d'alias
            alias_table, cs = table_building(objects.copy(), weights.copy())
            if not (alias_table): 
                print(f"Test {index_test}:")
                print("     La table n'a pas été construite..")
                print(f"     Liste des objet et leur poids: {dict(zip(objects, weights))}")
                continue
            
            # Generation des objets 
            generated = Counter(generation(alias_table, cs) for _ in range(num_samples))

            # Permet de gerer si on veut l'affichage ou non
            if check_frequencies(objects, weights, generated): # or check_last_cells(alias_table)
                printer = True

            if not(printer):  
                continue

            print(f"Test {index_test}:")
            print(f"    Liste des objet et leur poids: {dict(zip(objects, weights))}")
            print(f"    Table Alias construite: {alias_table}")
            print(f"    Cell size: {cs}")
            print(f"    Fréquences des objets générés (sur {num_samples} essais):")
          
            for obj, count in generated.items():
                print(f"        - {obj}: {count / num_samples:.2f} ({count} fois)")

            print("\n")

        except KeyboardInterrupt:
            print(f"Interruption détectée, {index_test} tests ont été executées")
            sys.exit(0)

        except Exception as e:
            print(f"Test {index_test}:")
            print(f"ERREUR: {e}")
            print(f"Liste des objet et leur poids: {dict(zip(objects, weights))}")
            
        

if __name__ == "__main__":
    #manual_tests()
    random_distributions_tests(10_000_000)
