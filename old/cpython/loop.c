#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_CPUS 64

void do_infinite_loop(int i ) {

  while(1) {
        // do nothing!
  }
}

int main(void) {
    int i;
    int n = 0;

    pthread_t thread[MAX_CPUS];

    for(i=0;i<MAX_CPUS;i++) {
        pthread_create(&thread[i] , NULL, (void *) do_infinite_loop, (void *) &i);
    }

    for(i=0;i<MAX_CPUS;i++) {
        pthread_join(thread[i], NULL);
    }

    return 0;
}
