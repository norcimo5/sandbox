#include <string>
#include <stdio.h>
#include <boost/lexical_cast.hpp>

using namespace std;

int main(void)
{
    string sNumber = "666.6";

    try {
    printf("%lf\n", boost::lexical_cast<double>(sNumber));
    }
    catch(boost::bad_lexical_cast) {
        printf("***SHABAMA***\n");
    };
    return 0;
}
