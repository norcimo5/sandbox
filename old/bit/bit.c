#include <stdio.h>

void binRep(int decimal)
{

  int i ;
  for(i = 0 ; i < sizeof(int) * 8; i++)
  {
    printf("%c", decimal & 0x80000000 ? '1' : '0');
    decimal = decimal << 1;
  }

  printf("\n");

}

int main(void)
{
  
  int a = 0x80818283;
  printf("Before: ");
  binRep(a);
  return 0;
  //a = a >> 3;
  //printf("After : ");
  //binRep(a);
  //return 0;

}
