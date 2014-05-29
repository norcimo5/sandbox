#ifndef __FORWARD_H_
#define __FORWARD_H_

typedef struct _forward forward; // forward declaration

typedef struct _complexity {
  forward *list; // THIS WORKS BECAUSE YOU CAN DO FORWARD DECLARATION FOR POINTERS ONLY. 
} complexity;

struct _forward {
  int x;
  int y;
  int z;
};

#endif // __FORWARD_H_
