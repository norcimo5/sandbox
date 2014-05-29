#ifndef __FUNCTION_TEMPLATE__
#define __FUNCTION_TEMPLATE__


/*
    FUNCTION TEMPLATES
*/
//template <class identifier> function_declaration;        // Function Template
//template <typename identifier> function_declaration;     // EXACTLY THE SAME THING AS <class identifier> function template

// EXAMPLE: MAX template. Note that if max(a,b ) instead of max<type>(a,b) , then it will call max <type> by argument deduction.
// This function template can be instantiated with any copy-constructible type for which the expression (y < x) is valid.
// For user-defined types, this implies that the less-than operator must be overloaded.
template <typename Type>
    Type max(Type a, Type b) {
    return a > b ? a : b;
    }

//template<>
    int max(int a, int b) {
    return a > b ? a : b;
    }
#endif
