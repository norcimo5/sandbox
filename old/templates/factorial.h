#ifndef __CLASS_TEMPLATE__
#define __CLASS_TEMPLATE__

// A class template provides a specification for generating classes based on parameters.
// Class templates are commonly used to implement containers.
// A class template is instantiated by passing a given set of types to it as template arguments.
// The C++ Standard Library contains many class templates, in particular the containers adapted
// from the Standard Template Library, such as vector.

// Example: Induction 
template <int N> 
struct Factorial {
      static const int value = N * Factorial<N - 1>::value;
};
 
// Base case via template specialization:
 
template <>
struct Factorial<0> {
      static const int value = 1;
};

template F Factorial<6>;

#endif

