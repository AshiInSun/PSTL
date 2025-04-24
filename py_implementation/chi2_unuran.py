import sys
import random
from collections import Counter
from unuran_alias import build_alias_table, sample_from_alias
from scipy.stats import chisquare


DEFAULT_SAMPLES = int(sys.argv[2]) if len(sys.argv) > 2 else 10000 
SIGNIFICANCE_LEVEL = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05

random.seed(1)

# Important: on test uniquement avec des poids entiers!!
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


def chi2_test(weights, observed, num_samples=DEFAULT_SAMPLES):
    
    # Fréquences attendues
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
        print("Usage : python chi2_unuran.py <fichier_distribution.txt>")
        sys.exit(1)

    filepath = sys.argv[1]
    weights = read_weights_from_file(filepath)

    print("\nDébut du test chi2 avec la méthode Alias (unuran)...")
    print("\n- Nombre de samples : ",DEFAULT_SAMPLES)
    print("- Niveau de signification : ",DEFAULT_SAMPLES)

    print(f"\n- Poids lus : {weights}")

    new_pv, alias_table = build_alias_table(weights)
    print(f"- Table alias : {alias_table}")
    print(f"- Probabilités ajustées : {new_pv}")

    samples = [sample_from_alias(new_pv, alias_table) for _ in range(DEFAULT_SAMPLES)]
    counts = Counter(samples)   
    observed = [counts.get(i, 0) for i in range(len(weights))] 

    chi2_test(weights, observed)