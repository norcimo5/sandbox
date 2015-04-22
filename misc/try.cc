#include <stdio.h>

int foo ( auto i, auto j ) { return (int)( i + j); }

int main(void) {

    printf("RES(%d, %d) =%d\n", 1, 5, foo(1, 5));

    return 0;
}
