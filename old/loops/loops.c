#include <stdio.h>


int main(int argc, char **argv)
{
  int i = 0;
  int j = 0;

  for (j = 0  ; j < 50 ; j++ ) {
    printf("i = %d \n", i);
    i = (++i & 7);
  }

  return 0;
}
