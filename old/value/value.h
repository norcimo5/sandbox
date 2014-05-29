#ifndef _VALUE_H_
#define _VALUE_H_
#include <cstdio>
class Value {
  public:
    Value(const int& something = 0) : m_something(something) { printf("[%s]: I was created!\n", __FUNCTION__);}
    Value(const Value&) { printf("[%s]: I was copied!\n", __FUNCTION__);}
    virtual ~Value(){printf("[%s]: I was destroyed!\n", __FUNCTION__);}

    Value& operator=(const Value&) { printf("[%s]: I was copy-assigned!\n", __FUNCTION__); return *this; }
    int getValue() const { return m_something; }
    void setValue(const int& something){ m_something = something; }

  private:
    int m_something;
};
#endif
