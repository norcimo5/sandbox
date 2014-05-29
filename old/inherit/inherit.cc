#include <stdio.h>

class Base {
  public:

  int a;

  Base(){ a = 1;}
  virtual ~Base(){ printf("[BASE]: DELETED\n");}

  int test(void){ return a;} 

};

class Derived : public Base {
  public:

  Derived(){}
  virtual ~Derived(){printf("[DERIVED]: DELETED\n");}


  int test(void) { return a+a;}

};

int main(void)
{
  Derived * d = new Derived();

  printf("%d\n", d->test());

  delete d;
  return 0;
}
