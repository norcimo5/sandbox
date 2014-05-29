#include <stdio.h>
#include <unistd.h>

void update(void) {
  printf("[UPDATING]");
  fflush(stdout);
}

void render(void) {
  printf("[RENDERING]");
  fflush(stdout);
}

int main(int argc, char * argv[])
{

  while(1) {
    update();
    render();
    sleep(1);

  }

  return 0;
}
