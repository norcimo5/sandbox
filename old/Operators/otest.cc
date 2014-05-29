#include <stdio.h>
#include <stdlib.h>
#include "otest.hh"


int main(int argc, char * argv[])
{
  Integer<unsigned long> i;

  i = 5;

  printf("%lu\n", i());

  i += 6;
  printf("%lu\n", i());

  i = i + 1;
  printf("%lu\n", i());

  return EXIT_SUCCESS;
}
