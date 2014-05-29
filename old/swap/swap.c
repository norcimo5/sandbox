#include <stdio.h>
#include <stdint.h>

typedef union {
  uint32_t word;
  uint8_t c[4];

} SWAP_T;

int main(void)
{
  SWAP_T num;

  int i;

  num.word = 0x01020304;

  printf("%.2xh\n", num.word); 

    num.word = (num.word << 24) |
    ((num.word <<  8) & 0x00ff0000) |
    ((num.word >>  8) & 0x0000ff00) |
    ((num.word >> 24) & 0x000000ff);

  printf("%.2xh\n", num.word); 

  for (i=0;i < 4;i++)
    printf("num.c[%d] = %.2xh\n", i, num.c[i]);


  return 0;

}
