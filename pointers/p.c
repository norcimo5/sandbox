#include <stdio.h>

typedef struct {
    int data;
} MYTYPE;

int main (void) {
    char data[] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 };
    int i;
    MYTYPE * x = (MYTYPE *) &data[0];

    for (i = 0; i < 6; i++){
        x = (MYTYPE *) &data[i];
        printf("%X:[%.8X]\n", i, x->data);
    }

    return 0;
}
