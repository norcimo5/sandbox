#include <stdio.h>
#include <stdlib.h>

void looper(void)
{
  static int count = 0;
  
  printf("%s:%s():%d ... ",__FILE__, __FUNCTION__, __LINE__);
  printf("Count = %d\n", count++);
  if (count == 5)
    return;
  else
    looper();
}

int main( int argc, char * argv[] )
{
  looper(); 
  return EXIT_SUCCESS;
}
