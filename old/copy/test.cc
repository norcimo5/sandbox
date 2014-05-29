#include <stdio.h>
#include <stdlib.h>
#include "uncopyable.hh"

int main(int argc, char *argv[])
{
  
  Uncopyable u;
  TestClass t;

  TestClass tt;

  tt = t;

  return EXIT_SUCCESS;
}
