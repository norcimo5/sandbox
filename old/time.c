#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>

int main(void)
{
    struct timeval startTime = {0,0};
    struct timeval currTime  = {0,0};
    gettimeofday(&startTime, NULL);

    usleep(50000);
    gettimeofday(&currTime, NULL);
    double elapsedTime = (double)(currTime.tv_sec - startTime.tv_sec) + (double)(currTime.tv_usec - startTime.tv_usec) / 1e6;
    printf("startTime    = %d, %d\n", startTime.tv_sec, startTime.tv_usec);
    printf("currTime     = %d, %d\n", currTime.tv_sec, currTime.tv_usec);
    printf("elapsedTime  = %lf\n", elapsedTime);

    return 0;
}
