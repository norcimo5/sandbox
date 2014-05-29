#include <stdio.h>
#include <string>

class Test {
    public:
        Test(const std::string& msg="") : _msg(msg) {}
        const std::string& getMessage() { return _msg; }

    private:
        std::string _msg;
};
