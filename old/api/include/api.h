// Copyright [2012] <Manuel A Perez>
#ifndef _HOME_MPEREZ_SANDBOX_API_INCLUDE_API_H_
#define _HOME_MPEREZ_SANDBOX_API_INCLUDE_API_H_
class Api {
  public:
    Api();                       // constructor
    Api(const Api&);             // copy constructor
    virtual ~Api();              // destructor

    Api& operator=(const Api&);  // copy assignment operator

  private:
};
#endif  // _HOME_MPEREZ_SANDBOX_API_INCLUDE_API_H_
