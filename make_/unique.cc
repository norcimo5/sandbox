#include <iostream>
#include <algorithm>
#include <memory>

using namespace std;

int main (void)
{
    auto s = std::make_unique<int[]>(5);
    auto a = std::vector<unique_ptr<int>>(s,5);
    //for( auto n : s )
    //  cout << "hello" << endl;

    return 0;
}
