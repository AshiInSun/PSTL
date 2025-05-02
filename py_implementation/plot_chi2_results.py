import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Répertoire contenant les fichiers de résultats
directory = "outputs"
files = sorted(f for f in os.listdir(directory) if f.startswith("results_chi2_test") and f.endswith(".csv"))

# Récupération des moyennes de chi² pour chaque fichier
labels = []
unuran_means = []
integer_means = []

for file in files:
    path = os.path.join(directory, file)
    df = pd.read_csv(path)
    
    moyennes = df[df.iloc[:, 0] == "Moyennes"]
    if not moyennes.empty:
        row = moyennes.iloc[0]
        labels.append(file.replace("results_chi2_test", "distribution ").replace(".csv", ""))
        unuran_means.append(row["Unuran_Chi2"])
        integer_means.append(row["Integer_Chi2"])

# Tracé du graphique
x = np.arange(len(labels))  # positions sur l'axe des x
width = 0.35  # largeur des barres

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - width/2, unuran_means, width, label='Alias Unuran')
bars2 = ax.bar(x + width/2, integer_means, width, label='Alias Entiers')

# Titres et étiquettes
ax.set_ylabel("Statistique $\chi^2$ moyenne")
ax.set_title("Comparaison des moyennes $\chi^2$ entre Alias Unuran et Entiers")
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend()

# Affichage des valeurs sur les barres (optionnel)
for bar in bars1 + bars2:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # décalage vertical
                textcoords="offset points",
                ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig("outputs/comparison_plot.png")
plt.show()
