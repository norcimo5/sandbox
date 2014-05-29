#include <stdio.h>

int main(void)
{
gl.glBegin(gl.GL_TRIANGLESTRIP);
gl.glVertex(100,100,−100);
gl.glVertex(100,300,−100);
gl.glVertex(300,300,−100);
 
gl.glVertex(300,300,−300);
gl.glVertex(300,100,−300);
 
gl.glVertex(100,100,−100);
gl.glVertex(100,100,−300);
 
gl.glVertex(100,300,−300);
gl.glVertex(100,300,−100);
 
gl.glVertex(100,300,−100);
gl.glVertex(100,300,−300);
 
gl.glVertex(100,100,−300);
gl.glVertex(300,100,−300);
gl.glEnd();
  return 0;
}
