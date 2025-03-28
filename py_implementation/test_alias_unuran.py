import sys
from collections import Counter
from unuran_alias import *

MAX_OBJECTS = 10                # Nombre maximum d'objets générés
MAX_WEIGHT = 100                # Poids maximum pour un objet
DEFAULT_TEST_AMOUNT = 100       # Nombre de tests par défaut
DEFAULT_SAMPLES = 1000          # Nombre d’échantillons générés par test
DEFAULT_TOLERANCE = 0.9         # Seuil de tolérance pour la vérification des distributions, par défaut à 1 car le comportement par défaut ne genere que 1 sample


def manual_tests():
    
    test_cases = [
        
        # NOTE Erreur non geré dans notre pseudo-code, est ce qu'il font un traitement special dans unnuran?
        #([], "Cas listes vides"),

        # NOTE Valide mais est ce qu'il font un traitement special dans unnuran quand ils ont des poids à 0? genre filtrage
        ([0, 1, 2], "Cas poids à 0"),

        # NOTE Erreur, ca genere la table mais les poids negatif ne devrait pas etre possible? traitement special dans unuran?
        ([-1, 1, 2], "Cas poids negatif"),

        # Valide
        ([3, 4, 5], "Cas simple avec 3 objets"),

        # Donne une table alias differente au test precedent bien que meme poids.
        ([3, 5, 4], "Cas simple avec 3 objets, ordre des poids different"),

        # Valide
        ([3, 4, 6], "Cas avec 3 objets mais dans l'alias integer on genere objet virtuel"),  

        # Valide
        ([1, 1, 1, 7], "Cas où un élément lourd est divisé en deux")       
        
        # Tests à ajouter
    ]
    for probs, description in test_cases:
        print(f"Test: {description}")

        try:
            print(f"    Liste des objet et leur poids: {probs}")
            print("    - Construction de la table Alias...")
            new_probs, alias_table = build_alias_table(probs)
            print(f"      Table Alias construite: {alias_table}")

            # Vérification de la génération aléatoire
            if alias_table:  
                print("    - Generation de 1000 tirages aleatoires...")
                samples = [sample_from_alias(new_probs, alias_table) for _ in range(1000)]
                print(f"      Echantillons générés: {dict(Counter(samples))}")
            print()
        
        except Exception as e:
            print(f"ERREUR: {e}")
            break

def random_distributions_tests(num_tests=DEFAULT_TEST_AMOUNT, num_samples=DEFAULT_SAMPLES,
                                seuil_tolerance=DEFAULT_TOLERANCE, printer=False):
    print("Génération de tests avec distribution aléatoire...")

    # FIXME pas correcte, à revoir.
    def check_frequencies(probabilities, generated):
        expected_frequencies = {i: p for i, p in enumerate(probabilities)}
        observed_frequencies = {i: generated.get(i, 0) / num_samples for i in range(len(probabilities))}

        for i in range(len(probabilities)):
            if abs(expected_frequencies[i] - observed_frequencies[i]) > seuil_tolerance:
                return True  # Problème détecté, affichage activé
            
        return False

    for index_test in range(1, num_tests + 1):
        try:
            # Génération aléatoire des probabilités
            num_objects = random.randint(2, MAX_OBJECTS)
            probabilities = [random.randint(1, MAX_WEIGHT) for _ in range(num_objects)]

            # Construction de la table Alias
            new_pv, alias_table = build_alias_table(probabilities)

            if not new_pv or not alias_table:
                print(f"Test {index_test}:")
                print("     La table n'a pas été construite..")
                print(f"    Probabilités: {probabilities}")
                continue

            # Génération d'échantillons aléatoires
            generated = Counter(sample_from_alias(new_pv, alias_table) for _ in range(num_samples))

            # Vérification des fréquences
            #printer = check_frequencies(new_pv, generated)

            # Affichage uniquement si problème détecté
            if not printer:
                continue

            print(f"Test {index_test}:")
            print(f"    Probabilités initiales: {probabilities}")
            print(f"    Table Alias: {alias_table}")
            print(f"    Probabilités ajustées: {new_pv}")
            print(f"    Fréquences des objets générés (sur {num_samples} essais):")

            for i, count in generated.items():
                print(f"        - Objet {i}: {count / num_samples:.2f} ({count} fois)")

            print("\n")

        except KeyboardInterrupt:
            print(f"Interruption détectée, {index_test} tests exécutés.")
            sys.exit(0)

        except Exception as e:
            print(f"Test {index_test}:")
            print(f"ERREUR: {e}")
            print(f"Probabilités: {probabilities}")
            
        

if __name__ == "__main__":
    #manual_tests()
    random_distributions_tests(10_000_000)
