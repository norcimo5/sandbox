#include<stdio.h>
#include <string>
#include "test.h"

int main(void)
{
    Test test("This is a test");
    const std::string& t = test.getMessage();

    printf("[%s]\n", t.c_str());

    return 0;
}
