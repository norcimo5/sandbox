#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int makeArray(const int n)
{
  int i;
  int a[n];

  for(i=0;i<n;i++) a[i] = i;

  return a[3];
}

int main(int argc, char * argv[])
{
  printf("%d\n",makeArray(5)); 

  return EXIT_SUCCESS;
}

