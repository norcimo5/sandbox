#include <stdio.h>

int main(void)
{
  unsigned int orig = 1;
  unsigned int shifted = 0;
  unsigned int i = 0;

  
  for(i = 1; i <= 16; i++) {

  shifted = (orig << i) ;

  printf("[%d] shifted %d times  to the left = %d\n", orig, i, shifted);
  }
  return 0;
}
