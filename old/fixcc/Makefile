# Generic C++ Makefile

CPP = g++
CPPFLAGS = -Wall
LDFLAGS = -m64

# Compile the fixcc.
fixcc : fixcc.cc
	$(CPP) $(CPPFLAGS) -o fixcc fixcc.cc $(LDFLAGS)

# Compile the fixcc to assembly
asm :
	$(CPP) $(CPPFLAGS) -S fixcc.cc $(LDFLAGS)
# command to be executed.
clean:
	rm -f fixcc
