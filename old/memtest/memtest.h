#ifndef __MEMTEST_H_
#define __MEMTEST_H_

typedef struct _memtest {

  char * bufferPtr;
} memtest;

void freePtr(void ** ptr);

#endif // __MEMTEST_H_
