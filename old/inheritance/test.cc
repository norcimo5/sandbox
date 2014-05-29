#include <string>
#include <iostream>

using namespace std;
class Employee
{
public:
    Employee(string name, string dept);
    virtual void print() const;
    string dept() const;
private:
    string _name;
    string _dept;
};

class Manager : public Employee
{
public:
    Manager(string name, string dept);
    virtual void print() const;
    string dept() const { return 0; }
private:
    // ...
};

void Employee::print() const
{   cout << _name << endl;
}

void Manager::print() const
{   Employee::print(); // print base class
    cout << dept() << endl;
}

int main(void)
{

  return 0;

}
