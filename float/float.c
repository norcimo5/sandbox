#include <stdio.h>


int main (int argc, char ** argv)
{
    float x = 0.3;
    double y = 0.3;

    if (x == 0.3) {
        printf("x = %lf\n", x);
        printf("y = %lf\n", y);
    } else {

    printf("Assertion incorrect! Can't print numbers :(\n");
    }
    return 0;
}
