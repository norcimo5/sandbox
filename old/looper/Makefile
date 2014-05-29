# Generic C++ Makefile

GCC = gcc
GCCFLAGS = -Wall
LDFLAGS = -S

# Compile the looper.
looper : looper.c
	$(GCC) $(GCCFLAGS) -o looper.asm looper.c $(LDFLAGS)

# command to be executed.
clean:
	rm -f looper.asm
