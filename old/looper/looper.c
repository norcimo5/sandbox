#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void loop (void)
{
  int loopTask = 1;

  while(loopTask) {
    printf("[ LOOPING ]\n");
    sleep(2);
  }
}

int main (int argc, char **argv)
{
  loop();
  return EXIT_SUCCESS;
}
