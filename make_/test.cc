#include <iostream>
#include <algorithm>
#include <memory>

using namespace std;

int main (void)
{
    auto a = std::make_shared<int>(7);
    cout << *a << endl;

    auto b = std::vector<int>({1,2,3,4,5});
    for( auto n : b )
      cout << n << endl;

    return 0;
}
