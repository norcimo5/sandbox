#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef union {
    unsigned char array[4];
    float f;
    unsigned int i;
} funion;

int printbin(unsigned int n) {
    int x = 31;

    puts("33222222222211111111110000000000");
    puts("10987654321098765432109876543210");
    puts("--------------------------------");

    for(; x >= 0; x--) {
        if ((n >> x) & 1) {
            printf("1");
        } else {
            printf("0");
        }
    }

    puts("");
}

int main (int argc, char *argv[]) {
    //unsigned int i = ((union { float f; unsigned int i; }){5}).i;
    //float f = ((union { unsigned int i; float f;}){5}).f;
    funion test = {0};
    if (argc < 2) return 0;
    test.f = strtod(argv[1],NULL);
    printf("[%f]\n", test.f);
    printf("[%d] ([0x%X])\n\n", test.i, test.i);

    printbin(test.i);

    return 0;
}
