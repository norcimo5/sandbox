# Generic C++ Makefile

CPP = gcc
CPPFLAGS = -Wall
LDFLAGS = -m32

# Compile the ctest.
ctest : ctest.c
	$(CPP) $(CPPFLAGS) -o ctest ctest.c $(LDFLAGS)

# command to be executed.
clean:
	rm -f ctest
