//float (*my_func_ptr)(int, char *);
// To make it more understandable, I strongly recommend that you use a typedef.
// Things can get particularly confusing when
// the function pointer is a parameter to a function.
// The declaration would then look like this:
typedef float (*MyFuncPtrType)(int, char *);
MyFuncPtrType my_func_ptr;


int main(void)
{

  return 0;
}
