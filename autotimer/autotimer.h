#include <string>
class AutoTimer {
  public:
    explicit AutoTimer(const std::string &name);
    ~AutoTimer();
  private:
    class Impl;
    Impl *mImpl;
};
