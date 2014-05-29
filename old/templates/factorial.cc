#include <stdio.h>
#include "function_template.h"

int main(void)
{
    printf("%lf\n", max<double>( 5, 4));
    return 0;
}
