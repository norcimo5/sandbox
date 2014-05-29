#include "vector3.h"

#include <stdio.h>
#include <stdlib.h>

int shazam(void* x){

  printf("This is just a test\n");
  return 0;
}

int main(int argc, char ** argv)
{
  Vector3 v;

  v.shazam = shazam;
  return EXIT_SUCCESS;
}
