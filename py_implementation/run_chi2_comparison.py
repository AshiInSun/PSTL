import sys
import csv
import os
import statistics
from chi2_unuran import run_chi2_test as run_unuran
from chi2_alias_integer import run_chi2_test as run_integer

def main():
    if len(sys.argv) < 2:
        print("Usage : python run_chi2_comparison.py <distribution_file.txt>")
        sys.exit(1)

    distribution_file = sys.argv[1]
    seeds = list(range(1, 31))  # Seeds de 1 à 30
    n_samples = 10000  # Nombre d'échantillons pour chaque test

    results_unuran = []
    results_integer = []

    for seed in seeds:
        print(f"Test chi2 en cours pour la seed : {seed}..")
        stat_unuran, pval_unuran = run_unuran(distribution_file, seed=seed, n_samples=n_samples)
        stat_integer, pval_integer = run_integer(distribution_file, seed=seed, n_samples=n_samples)

        results_unuran.append((stat_unuran, pval_unuran))
        results_integer.append((stat_integer, pval_integer))

    # Calcul des moyennes
    print(f"Calcul des moyennes...")
    mean_stat_unuran = statistics.mean(stat for stat, _ in results_unuran)
    mean_pval_unuran = statistics.mean(pval for _, pval in results_unuran)

    mean_stat_integer = statistics.mean(stat for stat, _ in results_integer)
    mean_pval_integer = statistics.mean(pval for _, pval in results_integer)

    # Calcul des écarts-types
    print(f"Calcul des écarts-types...")
    std_stat_unuran = statistics.stdev(stat for stat, _ in results_unuran)
    std_pval_unuran = statistics.stdev(pval for _, pval in results_unuran)

    std_stat_integer = statistics.stdev(stat for stat, _ in results_integer)
    std_pval_integer = statistics.stdev(pval for _, pval in results_integer)

    base_filename = os.path.splitext(os.path.basename(distribution_file))[0]
    output_csv = f"outputs/results_chi2_{base_filename}.csv"

    with open(output_csv, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Seed", "Unuran_Chi2", "Unuran_pvalue", "Integer_Chi2", "Integer_pvalue"])

        for i, seed in enumerate(seeds):
            writer.writerow([
                seed,
                round(results_unuran[i][0], 5),
                round(results_unuran[i][1], 5),
                round(results_integer[i][0], 5),
                round(results_integer[i][1], 5)
            ])

        # Ligne vide
        writer.writerow([])

        # Résumés
        writer.writerow(["Moyennes", round(mean_stat_unuran, 5), round(mean_pval_unuran, 5),
                         round(mean_stat_integer, 5), round(mean_pval_integer, 5)])

        writer.writerow(["Ecart-types", round(std_stat_unuran, 5), round(std_pval_unuran, 5),
                         round(std_stat_integer, 5), round(std_pval_integer, 5)])

    print(f"\n✅ Résultats enregistrés dans {output_csv}")

if __name__ == "__main__":
    main()
