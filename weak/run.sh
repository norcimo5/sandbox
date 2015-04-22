#!/bin/bash
echo -n "[ COMPILING ... "
/usr/bin/g++ -std=c++14 -O2 -Wall -Wextra -pedantic -pthread -pedantic-errors weak.cc -lm -o weak
echo "DONE ]"
./weak
