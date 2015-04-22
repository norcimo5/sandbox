#include <iostream>
#include <algorithm>
#include <memory>


using namespace std;

int main(void)
{
    auto p = make_shared<int[]>(5);

    for(auto i = 0 ; i < 5; i++){
      cout << p[i] << endl;
    }

    auto v = vector<shared_ptr<>>(p, p + 5 );
    return 0;
}
