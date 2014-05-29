#include <stdio.h>

int main(void)
{
    int i;
    unsigned char j[100] = {0};

    for(i = 0;i < 100; i++) {
        printf("%.2X%c", j[i], ((i+1) % 20) ? ' ' : '\n' );
    }

    return 0;
}
