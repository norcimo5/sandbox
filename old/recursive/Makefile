# Generic C++ Makefile

CPP = gcc
CPPFLAGS = -Wall
LDFLAGS = -m64

# Compile the recursive.
recursive : recursive.c
	$(CPP) $(CPPFLAGS) -o recursive recursive.c $(LDFLAGS)

# command to be executed.
clean:
	rm -f recursive
