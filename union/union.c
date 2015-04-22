#include <stdio.h>

typedef union {
    unsigned char byte[4];
    unsigned int word;
} WORDTYPE;

int main(int argc, char **argv) {
    unsigned char data[4] = {0};
    WORDTYPE x = &data;
    x->word = 1024*1024*1024+1031231;
    printf("%d, [ %.2X %.2X %.2X %.2X ]\n", x->word, x->byte[0], x->byte[1], x->byte[2], x->byte[3]);
    
    return 0;
}
