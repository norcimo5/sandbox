#include <stdio.h>
#include <stdlib.h>


int main(void)
{
  int i;
  i = -2147483648;
  printf("Integer before overflow=%d\n", i);
  i--;
  printf("Integer after  overflow=%d\n", i);
  return EXIT_SUCCESS;
}
