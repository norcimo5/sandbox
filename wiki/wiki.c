#include <stdio.h>
#include <stdlib.h>

int main(int argc, char * argv[]) {
  char strWiki[256] = {};

  if ( argc < 2 ) return 0;

  sprintf(strWiki, "/usr/bin/lynx -accept_all_cookies https://en.wikipedia.org/wiki/%s", argv[1]);
  return system(strWiki);
}
