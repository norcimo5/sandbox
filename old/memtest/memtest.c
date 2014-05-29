#include <stdio.h>
#include <stdlib.h>

#include "memtest.h"

//void freePtr(void ** ptr)
//{
//  if(*ptr) {
//    free(*ptr);
//    *ptr=NULL;
//  }
//}

#define freePtr(X) if((X)) {free((X)); (X)=NULL;}

int main(int argc, char **argv)
{
  memtest mtest = {0} ;

  printf("[ BEFORE FREE = %p ] \n", mtest.bufferPtr);

  mtest.bufferPtr = (char *) calloc(1, 2000 * 1024 * 1024);
  if(mtest.bufferPtr == NULL) {
    printf("[ ERROR: COULD NOT ALLOCATE MEMORY ] \n");
    return EXIT_FAILURE;
  } else {
    printf("[ SUCCESS! (%p) ] \n", mtest.bufferPtr);

  }

  freePtr(mtest.bufferPtr);

  printf("[ AFTER FREE = %p ] \n", mtest.bufferPtr);

  return EXIT_SUCCESS;
}
