#include <stdio.h>
#include "test.h"

int main(void)
{
int x{0}; 
for(int xx = 0; xx < 5; ++xx)
{
    startBenchmark();
{
    std::function<int(int)> t2 = [&x](int i){ return i + x; };
    std::function<void(int)> t1 = [&x, &t2](int i){ x = t2(i); };
    for(int i = 0; i < 1000000000; ++i) t1(i);
} lo << lt("std::func") << endBenchmark() << endl;

startBenchmark();
{
    delegate<int(int)> t2 = [&x](int i){ return i + x; };
    delegate<void(int)> t1 = [&x, &t2](int i){ x = t2(i); };
    for(int i = 0; i < 1000000000; ++i) t1(i);
    } lo << lt("ssvu::fastfunc") << endBenchmark() << endl;
}

return 0;

}
