#include <stdio.h>

class SomeClass {
   public: 
         virtual void some_member_func(int x, char *p) {
                  printf("In SomeClass"); };
};

class DerivedClass : public SomeClass {
   public:
      // If you uncomment the next line, the code at line (*) will fail!
     //    virtual void some_member_func(int x, char *p) { printf("In DerivedClass"); };
};

int main() {
      // Declare a member function pointer for SomeClass
      typedef void (SomeClass::*SomeClassMFP)(int, char *);
          SomeClassMFP my_memfunc_ptr;
              my_memfunc_ptr = &DerivedClass::some_member_func; // ---- line (*)
}
