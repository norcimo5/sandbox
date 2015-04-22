#!/usr/bin/python
def circle(x0, y0, radius):
  x = radius
  y = 0
  radiusError = 1 - x
  
  while x >= y:
    point( x + x0,  y + y0)
    point( y + x0,  x + y0)
    point(-x + x0,  y + y0)
    point(-y + x0,  x + y0)
    point(-x + x0, -y + y0)
    point(-y + x0, -x + y0)
    point( x + x0, -y + y0)
    point( y + x0, -x + y0)
    y = y + 1
    if radiusError < 0:
        radiusError = radiusError + ( 2 * y + 1 )
    else:
        x = x - 1
        radiusError = radiusError + (2 * (y - x + 1))
