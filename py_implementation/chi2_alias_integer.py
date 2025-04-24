import sys
import random
from collections import Counter
from alias_interger_weights import table_building, generation  
from scipy.stats import chisquare


DEFAULT_SAMPLES = int(sys.argv[2]) if len(sys.argv) > 2 else 10000 
SIGNIFICANCE_LEVEL = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05

random.seed(1)

def read_weights_from_file(filepath):
    try:
        with open(filepath, "r") as file:
            line = file.readline()
            if "," in line:
                return [int(x.strip()) for x in line.split(",")]
            else:
                return [int(x.strip()) for x in line.split()]
    except Exception as e:
        raise ValueError(f"Erreur de lecture du fichier '{filepath}': {e}")


def chi2_test(weights, observed):
    total_weight = sum(weights)
    expected = [DEFAULT_SAMPLES * (w / total_weight) for w in weights]

    print(f"\n- Fréquences observées : {observed}")
    print(f"- Fréquences attendues : {[round(e, 2) for e in expected]}")

    stat, p_value = chisquare(f_obs=observed, f_exp=expected)

    print(f"\n- Statistique du chi² : {stat:.3f}")
    print(f"- Valeur p : {p_value:.4f}")

    if p_value < SIGNIFICANCE_LEVEL:
        print("\n⚠️  La distribution générée diffère significativement de la distribution attendue.")
    else:
        print("\n✅ La distribution générée correspond bien à la distribution attendue.")
    print("\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python chi2_integer_alias.py <fichier_distribution.txt>")
        sys.exit(1)

    filepath = sys.argv[1]
    weights = read_weights_from_file(filepath)

    print("\nDébut du test chi² avec la méthode Alias (entiers)...")
    print("\n- Nombre de samples : ",DEFAULT_SAMPLES)
    print("- Niveau de signification : ",DEFAULT_SAMPLES)

    print(f"\n- Poids lus : {weights}")

    objects = [f"obj{i}" for i in range(len(weights))]
    table, cell_size = table_building(objects, weights.copy())

    print(f"- Table construite : {table}")
    print(f"- Taille de cellule : {cell_size}")

    samples = [generation(table, cell_size) for _ in range(DEFAULT_SAMPLES)]
    counts = Counter(samples)
    observed = [counts.get(f"obj{i}", 0) for i in range(len(weights))]

    chi2_test(weights, observed)
