#include <stdio.h>

int main(void)
{

  int x = 0;
  int y = 0;
  int z = 0;
  int i = 0;
  int j = 0;

    for ( z = 0 ; z < 6; z++ ) 
      for ( y = 0 ; y < 3; y++ )
        for ( x = 0 ; x < 3; x++ ){
          int dx = x * 320;
          int dy = y * 320;
          int dz = z * 160;
          printf("<item>%d %d %d</item>\n", -400 + dx, -400 +dy, -400 + dz);
          printf("<item>%d %d %d</item>\n", -240 + dx, -400 +dy, -400 + dz);
          printf("<item>%d %d %d</item>\n", -240 + dx, -240 +dy, -400 + dz);
          printf("<item>%d %d %d</item>\n", -400 + dx, -240 +dy, -400 + dz);
  }

  for ( i = 0 ; i < 54; i++) {
    j = i * 4;
    printf("<item>%d %d</item>\n", j + 0, j + 1);
    printf("<item>%d %d</item>\n", j + 1, j + 2);
    printf("<item>%d %d</item>\n", j + 2, j + 3);
    printf("<item>%d %d</item>\n", j + 3, j + 0);
  }

  for(i = 0; i < 36; i++) {
    printf("<item>%d %d</item>\n", i , i + 36);
    printf("<item>%d %d</item>\n", i + 72 , i + 108);
    printf("<item>%d %d</item>\n", i + 144 , i + 180);
    
  }

  return 0;
}
