#include <stdio.h>
#include <stdlib.h>
#include <boost/shared_ptr.hpp>

void free_as_in_freedom(void *ptr)
{
  printf("[%p] is FREE!\n", ptr);
  free(ptr);
}

boost::shared_ptr<char> shared_strdup(const char* str)
{
  boost::shared_ptr<char> rval(strdup(str), free_as_in_freedom);
  return rval;
}

int main(int argc, char * argv[])
{

  boost::shared_ptr<char> s = shared_strdup("Hello World!");

  printf("[%s]\n", s.get());

  return EXIT_SUCCESS;
}

