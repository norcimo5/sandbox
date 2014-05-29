#include <stdio.h>
#include <time.h>
#include <sys/time.h>

int main(void)
{
    const double timeoutMSec = 100.0; // 100ms
    double m_startTimeSec = 1351780920.0;
    double m_startTimeNSec = 0;
    struct timeval currTime = {0,0};
    gettimeofday(&currTime, NULL);
    //double elapsedTime = ((double)currTime.tv_sec - m_startTimeSec) * 1e3 + ((double)currTime.tv_usec / 1e3) - (m_startTimeNSec / 1e6);
    double elapsedTime = ((double)currTime.tv_sec - m_startTimeSec) * 1e9 + ((double)currTime.tv_usec * 1e3) - m_startTimeNSec;

    printf("Current time = %lf sec, %1f us, %1f ms\n", (double)currTime.tv_sec, (double)currTime.tv_usec, (double)currTime.tv_usec / 1e3);

    printf("%lf\n", elapsedTime);

    return 0;
}
