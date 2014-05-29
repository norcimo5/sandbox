#include <stdio.h>

typedef struct {
    int x;
    int y;
    int z;
} testType;

int main(void)
{
  testType t = { 1, -1, 0 };

  printf ("%d, %d, %d\n", t.x, t.y, t.z );

  return 0;
}
