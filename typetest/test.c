#include <stdio.h>

int main (int argc, char ** argv)
{
    goto shabama;
    //goto label2;
    //goto label3;
    return 0;
}

void test_one (void) {
shabama:
  printf("This is test one\n");
}

void test_two (void) {
label2:
  printf("This is test two\n");
}

void test_three (void) {
label3:
  printf("This is test three\n");
}

