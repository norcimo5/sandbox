#include <tuple>
#include <stdio.h>

using namespace std;
std::tuple<int, bool, float> foo()
{
	return make_tuple(128, true, 1.5f);
}

int main()
{
	int obj1;
	bool obj2;
	float obj3;

	std::tie(obj1, obj2, obj3) = foo();

  printf("%d, %s, %f\n", obj1, obj2 ? "true" : "false", obj3);
}
