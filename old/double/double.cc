#include <stdio.h>
#include <stdint.h>

uint64_t test(void) {

  return 20000L;
}

double test2(void) {

  return test();
}

int main (void)
{
  
  printf("%lu\n", test());
  printf("%f\n", test2());
  return 0;

}
