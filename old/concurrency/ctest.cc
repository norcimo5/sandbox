#include <iostream>
#include <thread>
#include <boost/thread.hpp>

int main()
{
    std::cout << std::thread::hardware_concurrency() << std::endl;
    std::cout << boost::thread::hardware_concurrency() << std::endl;
    return 0;
}
