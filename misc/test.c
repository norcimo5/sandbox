#include <stdio.h>
#include <string.h>

int main(void)
{
    int num = 0;
    char * text = "Sample text";
    for (int i = 0, num = strlen(text); i < num; i++)
      printf("%c\n", text[i]);
    return 0;
}
