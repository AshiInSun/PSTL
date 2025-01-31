// Creator:  --, --
// On the work of -- and --
// On the alias Algorithm of A. J. Walker


#include <stdio.h>
#include <malloc.h>


int(*alias_table(int *objects, int objects_size, int *weights, int weights_size))[3] {
    int n = objects_size;
    int total_weight = 0;
    for (int i = 0; i < weights_size; i++) {
        total_weight += weights[i];
    }
    int cell_size = total_weight / n;
    int rest = total_weight % n;
    int (*table)[3] = malloc(n * sizeof(*table));

    //extend the listes if the sum of the weights is not a multiple of the number of objects
    if(rest>0){
        n++;
        table = realloc(table, n * sizeof(*table));
        objects = realloc(objects, n * sizeof(int));
        weights = realloc(weights, n * sizeof(int));
        objects[n-1] = -1;
        weights[n-1] = cell_size - rest;
        total_weight += cell_size - rest;
    }

    int m = total_weight / n;
    int *heavy_stack = malloc(n+1 * sizeof(int));
    int *light_stack = malloc(n+1 * sizeof(int));
    int size_heavy = 0;
    int size_light = 0;

    for (int i = 0; i < n; i++) {
        if (weights[i] >= m) {
            heavy_stack[size_heavy] = i;
            size_heavy++;
        } else {
            light_stack[size_light] = weights[i];
            size_light++;
        }
    }
    heavy_stack[size_heavy] = -1;
    light_stack[size_light] = -1;
    size_heavy++;
    size_light++;
    int k = 0;

    //Ici on a un LIFO au lieu d'une FIFO mais ça ne devrait pas poser de problème. Il est néanmoins important de le noter, pour nos tests semi-aléatoires futures.
    while(size_heavy>0){
        int i = heavy_stack[size_heavy-1];
        size_heavy--;
        int heavy_obj = objects[i];
        int heavy_weight = weights[i];

        if(size_light>0){
            int j = light_stack[size_light-1];
            size_light--;
            int light_obj = objects[j];
            int light_weight = weights[j];

            if(light_obj!=-1){
                table[k][0] = light_weight;
                table[k][1] = light_obj;
                table[k][2] = heavy_obj;
            }else{
                table[m-1][0] = light_weight;
                table[m-1][1] = light_obj;
                table[m-1][2] = heavy_obj;
            }
            weights[i] -= light_weight;
        }else{
            table[k][0] = cell_size;
            table[k][1] = heavy_obj;
            table[k][2] = -1;
            weights[i] -= cell_size;
        }

        if(weights[i]<cell_size && weights[i]>0){
            light_stack[size_light] = i;
            size_light++;
        }else if(weights[i]>=cell_size){
            heavy_stack[size_heavy] = i;
            size_heavy++;
        }
        k++;
        //fin boucle while
    }
    if(k==m-2){
        int i = light_stack[size_light-1];
        size_light--;
        int light_obj = objects[i];
        int light_weight = weights[i];
        int j = light_stack[size_light-1];

    }

    return table;
}


int main() {


}
