#include<stdio.h>
#include <sys/time.h>
 
#define TOGETHER (8)
double getCurrTime (void) {
    struct timeval t = {0};
    gettimeofday(&t, NULL);
    return ( (double) t.tv_sec + ( (double) t.tv_usec / 1000000.0) );
} 

int main(void)
{ 

 int i = 0; 
 int entries = 56;                                 /* total number to process     */
 int repeat;                                       /* number of times for while.. */
 int left = 0;                                     /* remainder (process later)   */ 
 struct timeval t = {0};
 double start_time = getCurrTime();

 /* If the number of elements is not be divisible by BLOCKSIZE,                   */ 
 /* get repeat times required to do most processing in the while loop             */
 
 repeat = (entries / TOGETHER);                    /* number of times to repeat   */
 left  =  (entries % TOGETHER);                    /* calculate remainder         */
 
 /* Unroll the loop in 'bunches' of 8                                             */ 
 while( repeat-- > 0 ) 
  { 
    printf("process(%d)\n", i    );
    printf("process(%d)\n", i + 1); 
    printf("process(%d)\n", i + 2); 
    printf("process(%d)\n", i + 3); 
    printf("process(%d)\n", i + 4); 
    printf("process(%d)\n", i + 5); 
    printf("process(%d)\n", i + 6); 
    printf("process(%d)\n", i + 7);
 
    /* update the index by amount processed in one go                            */ 
    i += TOGETHER; 
  }
 
 /* Use a switch statement to process remaining by jumping to the case label     */ 
 /* at the label that will then drop through to complete the set                 */ 
 switch (left) 
  {
     case 7 : printf("process(%d)\n", i + 6);      /* process and rely on drop through */
     case 6 : printf("process(%d)\n", i + 5); 
     case 5 : printf("process(%d)\n", i + 4);  
     case 4 : printf("process(%d)\n", i + 3);  
     case 3 : printf("process(%d)\n", i + 2); 
     case 2 : printf("process(%d)\n", i + 1);      /* two left                                      */
     case 1 : printf("process(%d)\n", i    );      /* just one left to process                      */ 
     case 0 :                               ;      /* none left                                     */
  } 

  printf("Start time = %lf\n", start_time);
  printf("Elapsed time = %lf\n", (getCurrTime() - start_time));
}
