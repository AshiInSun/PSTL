# chi2_unuran.py
import sys
import random
from collections import Counter
from unuran_alias import build_alias_table, sample_from_alias
from scipy.stats import chisquare

DEFAULT_SAMPLES = 10000

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

def run_chi2_test(filepath, seed=1, n_samples=DEFAULT_SAMPLES):
    random.seed(seed)
    weights = read_weights_from_file(filepath)

    new_pv, alias_table = build_alias_table(weights)

    samples = [sample_from_alias(new_pv, alias_table) for _ in range(n_samples)]
    counts = Counter(samples)
    observed = [counts.get(i, 0) for i in range(len(weights))]

    total_weight = sum(weights)
    expected = [n_samples * (w / total_weight) for w in weights]

    stat, p_value = chisquare(f_obs=observed, f_exp=expected)

    return stat, p_value

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python chi2_unuran.py <fichier_distribution.txt> [seed] [n_samples]")
        sys.exit(1)

    filepath = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    n_samples = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_SAMPLES

    stat, p_value = run_chi2_test(filepath, seed, n_samples)
    print(f"Stat: {stat:.3f}, p-value: {p_value:.4f}")
