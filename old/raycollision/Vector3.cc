#include <stdio.h>
#include "Vector3.h"


int main(void)

{
  Vector3 v;
  printf("Size = %d\n", sizeof(Vector3));
  printf("Size = %d\n", sizeof(v));
  v.x=5;
  v.y=3;
  printf("x=%f\n", v[1]+v[0]);
  v[0]=5;
  printf("v[0]=%f\n", v[0]);
  return 0;
}
