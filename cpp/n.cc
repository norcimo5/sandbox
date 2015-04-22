#include <iterator>
#include <vector>
#include <cstdio>

using namespace std;

int main(int argc, char * argv[])
{
  int sum = 0;
  int nn[] = {1, 2, 3, 4, 5};

  vector<int> numbers(nn, nn + sizeof(nn) / sizeof(int));

  for(auto n: numbers)
    sum += n;

  printf("[%d]\n", sum);

  return 0;
}
