#ifndef _COPY_H_
#define _COPY_H_

class Uncopyable {
  public:
    Uncopyable(){}
    virtual ~Uncopyable(){}

  private:
    Uncopyable(const Uncopyable&);
    Uncopyable& operator=(const Uncopyable&);
};

class TestClass : Uncopyable {
  public: 
   TestClass():a_(0){}
   ~TestClass(){}

   int getA() { return a_; }
   void setA(int a) { a_ = a;}

  private:
   int a_;


};
#endif
