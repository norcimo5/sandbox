#include <stdio.h>
#include "singleton.h"

using namespace mperez;
int main(int argc , char * argv[])
{
  MySingleton::instance()->setMoney(5);
  printf("mySingleton Instance pointer = %p\n", MySingleton::instance());
  printf("Money = %d\n", MySingleton::instance()->getMoney());
  return 0;
}
