#include <stdio.h>
#include <string>
#include <boost/shared_ptr.hpp>

int main(void)
{
    int test1;
    boost::shared_ptr<int> test2;
    test2 = &test1;
    return 0;
}
