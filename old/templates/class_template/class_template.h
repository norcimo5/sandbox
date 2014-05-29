#ifndef __CLASS_TEMPLATE__
#define __CLASS_TEMPLATE__

// A class template provides a specification for generating classes based on parameters.
// Class templates are commonly used to implement containers.
// A class template is instantiated by passing a given set of types to it as template arguments.
// The C++ Standard Library contains many class templates, in particular the containers adapted
// from the Standard Template Library, such as vector.

// Example:
template <class A_Type> class calc
{
      public:
              A_Type multiply(A_Type x, A_Type y);
              A_Type add(A_Type x, A_Type y);
};
template <class A_Type> A_Type calc<A_Type>::multiply(A_Type x,A_Type y)
{
      return x*y;
}

template <class A_Type> A_Type calc<A_Type>::add(A_Type x, A_Type y)
{
      return x+y;
}

template <>
class calc
{
      public:
              string add(string x, string y) { printf("Shabama!!!\n");  return x;}
};

#endif

