#include <memory>
#include <boost/shared_ptr.hpp>

#define DECLARE_SINGLETON_FRIENDS( X ) \
      friend class mperez::singleton< X >; \
      friend class boost::shared_ptr< X >;

namespace mperez {
  template< typename T > class singleton 
  {
    protected:
  
    static const boost::shared_ptr< T > _instance;
  
    singleton();
    virtual ~singleton();
  
    public:
    static T* instance() 
    {
      return _instance.get();
    }
  };
  
  template< typename T > const boost::shared_ptr<T> singleton<T>::_instance( new T ); // Note: This makes it available always !!!
  
  template< typename T > singleton< T >::singleton()
  {
  }
  
  template< typename T > singleton< T >::~singleton()
  {
  }

}

class MySingleton : public mperez::singleton< MySingleton >
{ 

  DECLARE_SINGLETON_FRIENDS( MySingleton );

  private:
    int _money;

  public: 
    int getMoney() { return _money; }
    void setMoney(int money) { _money = money; }

};
