#include <stdio.h>

typedef union {
  unsigned char a[4];
  float f;
  unsigned int i;
} funion;

int main(void) {
    funion test = {0};
    test.i = 0b00111110001000000000000000000000;
    printf("%u\n", test.i);
    printf("%f\n", test.f);
    return 0;
}
