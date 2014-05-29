#ifndef _VECTOR_3_
#define _VECTOR_3_

#ifndef __cplusplus
//-----------------------------------------------------------------
// C VERSION
// structure with supporting functions
typedef struct {
  int (* const shazam)(void *test);
  union {
    struct {
      float x,y,z;
    };
    float list[3];
  };
} Vector3;
#else
//-----------------------------------------------------------------
// C++ VERSION
// class template with methods

//-----------------------------------------------------------------

#endif // __cplusplus
#endif // _VECTOR_3_
