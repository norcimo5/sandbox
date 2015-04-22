# Generic C++ Makefile

CPP = g++
CPPFLAGS = -Wall
LDFLAGS = -m64 -std=c++11

# Compile the hello.
hello : hello.cc
	$(CPP) $(CPPFLAGS) -o hello hello.cc $(LDFLAGS)

# command to be executed.
clean:
	rm -f hello
