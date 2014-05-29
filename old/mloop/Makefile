# Generic C++ Makefile

CPP = g++
CPPFLAGS = -Wall
LDFLAGS  = -std=c++11 -lpthread

# Compile the mloop.
mloop : mloop.cc
	$(CPP) $(CPPFLAGS) -o mloop mloop.cc $(LDFLAGS)

# command to be executed.
clean:
	rm -f mloop
