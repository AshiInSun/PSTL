#include <iostream>
#include <vector>
#include <string>
#include <tuple>
#include <stdexcept>
#include <random>
#include <algorithm>

using AliasCell = std::tuple<int, std::string, std::string>;
constexpr const char* VIRTUAL_OBJECT_NAME = "virtual_object";



std::pair<std::vector<AliasCell>, int> table_building(std::vector<std::string> objects, std::vector<int> weights) {
/**
 * @brief Constructs an alias table for generating discrete random variables based on integer weights.
 *
 * @param objects Vector of distinct object names to randomly sample from.
 * @param weights Corresponding positive integer weights for each object.
 *
 * @return A pair:
 *         - Alias table: A vector of (w, x, x') triplets where:
 *           - w is a threshold weight,
 *           - x is the primary object,
 *           - x' is the alias (fallback) object.
 *         - cell_size: The normalized cell size used in the alias method.
 *
 * @throws std::invalid_argument If inputs are empty, of different sizes, or contain negative weights.
 *
 * Notes:
 * - Adds a virtual object if the total weight isn't divisible by the number of objects,
 *   ensuring a uniform cell size.
 * - Designed for use with the `generation()` function.
 * - You can find a detailled report in github.com/AshiInSun/PSTL
 */

    //Entry check
    if (objects.empty() || weights.empty()) {
        throw std::invalid_argument("Les listes 'objects' et 'weights' ne peuvent pas être vides");
    }

    if (objects.size() != weights.size()) {
        throw std::invalid_argument("Les listes 'objects' et 'weights' doivent être de même taille");
    }

    for (int w : weights) {
        if (w < 0) throw std::invalid_argument("Les poids doivent être des entiers positifs");
    }
    for (std::string o : objects){
        if(o==VIRTUAL_OBJECT_NAME) throw std::invalid_argument("An object should not be \"virtual_object\".");
    }

    //Initialization
    int n = objects.size();
    int total_weight = std::accumulate(weights.begin(), weights.end(), 0);
    int cell_size = total_weight / n;
    int rest = total_weight % n;
    int r = total_weight % cell_size;

    //Add a virtual object to the list. You can reffer to the report for more details on the utility of that object.
    if (r > 0) {
        objects.emplace_back(VIRTUAL_OBJECT_NAME);
        weights.push_back(cell_size - r);
        total_weight += cell_size - r;
    }
    //Init the rich/poor tables
    int m = total_weight / cell_size;
    std::vector<AliasCell> table(m);
    std::vector<int> rich_stack, poor_stack;
    for (int i = 0; i < weights.size(); ++i) {
        if (weights[i] >= cell_size) rich_stack.push_back(i);
        else poor_stack.push_back(i);
    }
    int k = 0;

    //Core of the algorithm
    while (!rich_stack.empty()) {
        int i = rich_stack.back(); rich_stack.pop_back();
        std::string rich_obj = objects[i];
        int& rich_weight = weights[i];

        if (!poor_stack.empty()) {
            int j = poor_stack.back(); poor_stack.pop_back();
            std::string poor_obj = objects[j];
            int poor_weight = weights[j];

            if (poor_obj !=  VIRTUAL_OBJECT_NAME) {
                table[k] = AliasCell(poor_weight, poor_obj, rich_obj);
            } else {
                table[m - 1] = AliasCell(cell_size - poor_weight, rich_obj, poor_obj);
                k--;
            }
            rich_weight -= (cell_size - poor_weight);
        }else{
            //Poor stack is empty. The cell is filled with a rich object, which we subtract the size of the cell.
            table[k] = AliasCell(cell_size, rich_obj, "");
            rich_weight -= cell_size;
        }
        //We verify if our rich object is now poor, if yes it is put in the poor_stack else it is reput in the rich_stack
        if (rich_weight > 0 && rich_weight < cell_size) poor_stack.push_back(i);
        else if (rich_weight >= cell_size) rich_stack.push_back(i);

        ++k;
    }
    return {table, cell_size};
}

std::string generation(const std::vector<AliasCell>& table, int cell_size) {

    /**
 * @brief Generates a random object from a given alias table.
 *
 * @param table Alias table built by `table_building()`.
 * @param cell_size The cell size returned by `table_building()`.
 *
 * @return A randomly selected object according to the distribution encoded in the alias table.
 *
 * Notes:
 * - The virtual object (if present) is excluded from selection.
 */
    size_t size = table.size();
    size_t total_weight = size * cell_size;

    //We verify if there is a virtual object in the table. If yes, we make sure to not draw it.
    AliasCell cell = table.back();
    int last_weight = std::get<0>(cell);
    std::string potential_xn = std::get<2>(cell);

    if (potential_xn == VIRTUAL_OBJECT_NAME) {
        int xn_weight = cell_size - last_weight;
        total_weight -= xn_weight;
    }

    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, total_weight - 1);
    int rand_value = dis(gen);

    int index = rand_value / cell_size;

    AliasCell ac = table[index];
    int w = std::get<0>(ac);
    std::string obj1 = std::get<1>(ac);
    std::string obj2 = std::get<2>(ac);

    std::string result = (rand_value % cell_size < w) ? obj1 : obj2;
    return result;
}