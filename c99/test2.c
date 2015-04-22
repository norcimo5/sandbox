#include <stdio.h>

int main(int argc, char ** argv)
{

    typedef struct { 
        int tacos;
        int burritos;
    } texmex;


    texmex t = {
        .burritos = 55,
    };

    printf("%d\n%d\n", t.tacos, t.burritos);

    return 0;
}
