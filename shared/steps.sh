#!/bin/bash
gcc -fPIC -g -c -Wall a.c
gcc -fPIC -g -c -Wall b.c
gcc -shared -Wl,-soname,libmystuff.so.1 \
          -o libmystuff.so.1.0.1 a.o b.o -lc
gcc -o test main.c -ldl
