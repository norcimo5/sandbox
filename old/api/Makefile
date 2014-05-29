# Generic C++ Makefile

CPP = g++
CPPFLAGS = -Wall
LDFLAGS = -m32

# Compile the api.
api : api.cc
	$(CPP) $(CPPFLAGS) -o api api.cc $(LDFLAGS)

# command to be executed.
clean:
	rm -f api
