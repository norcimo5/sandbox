# Generic C++ Makefile

CPP = g++
CPPFLAGS = -Wall
LDFLAGS  = -std=c++11 -lboost_thread-mt -lpthread

# Compile the ctest.
ctest : ctest.cc
	$(CPP) $(CPPFLAGS) -o ctest ctest.cc $(LDFLAGS)

# command to be executed.
clean:
	rm -f ctest
