#include <stdio.h>
#include <stdlib.h>
#include "ctest.h"

Ctest foo(void)
{
  Ctest c;
  c.x= 1;
  c.y= 2;
  c.z= 3;
  printf("c.x pointer = %p\n", &(c.x));
  return c;
}
int main(int argc, char *argv[])
{
  Ctest ctest = foo(); 

  printf("ctest.x pointer = %p\n", &(ctest.x));
  printf("[%d,%d,%d]\n", ctest.x, ctest.y, ctest.z);

  return EXIT_SUCCESS;
}
