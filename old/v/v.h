#ifndef _V_H_
#define _V_H_
#include <vector>

class Test {

  public:
    Test() {}
    virtual ~Test() {}
    


  private:
    Test(const Test&);
    Test& operator=(const Test&);

    std::vector<int> _vec;

};
#endif
