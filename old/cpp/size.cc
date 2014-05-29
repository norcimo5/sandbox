#include <stdio.h>


int main(void) {

    char a[] = "This is just a test";

    int size = sizeof(a)/sizeof(a[0]);

    printf("%d\n", size);

    return 0;
}
