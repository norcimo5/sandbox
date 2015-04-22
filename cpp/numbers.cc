#include <iterator>
#include <vector>
#include <cstdio>

using namespace std;

void printVector(vector<int> v) {
  printf("[");  
  for(auto n: v)
    printf(" %d,", n );
  printf(" ]\n");  
}

int main(int argc, char * argv[])
{
  int sum = 0;
  int nn[] = {1, 2, 3, 4, 5};

  vector<int> numbers(nn, nn + sizeof(nn) / sizeof(int));

  printVector(numbers);

  for(auto n: numbers)
    sum += n;

  printf("[%d]\n", sum);

  return 0;
}
