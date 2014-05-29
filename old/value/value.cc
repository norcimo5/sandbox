#include <cstdio>
#include <cstdlib>

#include "value.h"

Value testfunction()
{
  Value z(5);
  return z;
}

int main(int argc, char *argv[])
{
  Value v = testfunction();
  Value x;
  x = v;
  printf("[%d]\n", v.getValue());
  return EXIT_SUCCESS;
}
