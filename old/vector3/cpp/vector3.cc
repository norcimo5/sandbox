#include <stdio.h>

class Vector3 {
  public:
  union {
    struct {
      float x; // 4 bytes = 32 bits
      float y;
      float z;
    };
    float a[3];
  };

  virtual void abc(){ printf("hello!!!\n"); }
  virtual void abcd(){ printf("hello!!!\n"); }

};

int main(void)
{
  Vector3 t;
  printf("size = %d bytes for class\n", sizeof(Vector3));
  printf("size = %d bytes for object\n", sizeof(t));

  t.x=1;
  t.y=2;
  t.z=5;

  for(int i=0;i<3;i++)
      printf("a[%d]=%f\n",i, t.a[i]);

  return 0;
}
