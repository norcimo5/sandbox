#include <stdio.h>

int main(void){
    unsigned char symbols[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567899`~!@#$%^&*()_-+={}[]\\|:;\"'<>,.?/";
    unsigned char result[7] = {0};
    unsigned long i;
    unsigned long len = sizeof(symbols) - 1;

    int index = 6;
    unsigned long dec = 1;
    int j;
    for (j = 0; j < 6; j++) {
        dec *=95L;
    }
    --dec;
    printf("%li\n", dec);
    i = dec;
    do {
        int ii = i - len * (i / len);
        printf("%li, %c\n", i % len , symbols[ ii ]);
        result[--index] = symbols[ ii];
        i /= len;
    } while ( i > 0  || index != 0);
    result[6] = '\0';
    puts("");
    printf("Result = [ %s ]\n",  result);

    return 0;
}
