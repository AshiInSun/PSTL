#include <iostream>
#include <unordered_map>
#include "alias_integer.cpp"

int main() {
    // Données d'entrée
    std::vector<std::string> objects = {"a", "b", "c"};
    std::vector<int> weights = {1, 3, 6}; // Probabilités : 10%, 30%, 60%

    // Construction de la table d'Alias
    auto [table, cell_size] = table_building(objects, weights);

    // Simulation
    int trials = 100000;
    std::unordered_map<std::string, int> frequency;

    for (int i = 0; i < trials; ++i) {
        std::string result = generation(table, cell_size);
        frequency[result]++;
    }

    // Affichage des résultats
    std::cout << "Résultats après " << trials << " tirages :\n";
    for (const auto& [key, count] : frequency) {
        double percent = (100.0 * count) / trials;
        std::cout << "Objet : " << key << " -> " << count << " (" << percent << "%)\n";
    }

    return 0;
}
