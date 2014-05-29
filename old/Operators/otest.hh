#ifndef _OTEST_HH_
#define _OTEST_HH_

template <class T>
class Integer {

  public:
    Integer() {}
    virtual ~Integer() {}

    const T getInteger() { return i_; }
    void setInteger(const T i) { i_ = i; }

    void operator =(const T i) { i_ = i; }

    Integer& operator +( const T r ) { this->operator+=(r); return *this; }
    Integer& operator +=( const T i ) { i_ += i; return *this; }

    T operator()() const { return i_; };

  private:
    T i_;
};

#endif
