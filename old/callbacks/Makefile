# Generic C++ Makefile

CPP = g++
CPPFLAGS = -Wall
LDFLAGS  = -std=c++11

# Compile the callbacks.
callbacks : callbacks.cc
	$(CPP) $(CPPFLAGS) -o callbacks callbacks.cc $(LDFLAGS)

# command to be executed.
clean:
	rm -f callbacks
