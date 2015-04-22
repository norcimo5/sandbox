#include <iostream>

using namespace std;

int main()
{
    return [] { cout << "Hello, my geeky friends" << endl; return 0; }();
}
