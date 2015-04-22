#include<stdio.h>
#include <string.h>

int verified_pass(const char * pwd) {
    const char pass[9] = "password";
    if (strncmp(pwd, pass, strlen(pass)) == 0)
        return 1;
    else
        return 0;
}

int main(void) {
    char test[2048] = {0};

    printf("Please enter password: ");
    fgets(test, 2048, stdin);
    if (verified_pass(test))
        puts("Passed!\n");
    else
        puts("Failed!\n");

    return 0;
}
