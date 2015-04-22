#include <iostream>

using namespace std;

void oldWay( int i) {
  i += 5;
}

void newWay ( const int & i ) {
//  i += 5;
}

int main (void)
{
  int n = 6;
  oldWay( n );
  cout << n << endl;

  newWay( n );
  cout << n << endl;
  return 0;
}
