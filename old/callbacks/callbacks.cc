#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>

template<typename TFuncSignature>
class Callback;

template<typename R, typename ... Args>
class Callback<R(Args...)> {
public:
	typedef R (*TFunc)(void*, Args...);

	Callback() :
			obj(0), func(0) {
	}
	Callback(void* o, TFunc f) :
			obj(o), func(f) {
	}

	R operator()(Args ... a) const {
		return (*func)(obj, std::forward<Args>(a)...);
	}
	typedef void* Callback::*SafeBoolType;
	operator SafeBoolType() const {
		return func ? &Callback::obj : 0;
	}
	bool operator!() const {
		return func == 0;
	}
	bool operator==(const Callback<R(Args...)>& right) const {
		return obj == right.obj && func == right.func;
	}
	bool operator!=(const Callback<R(Args...)>& right) const {
		return obj != right.obj || func != right.func;
	}
private:
	void* obj;
	TFunc func;
};

namespace detail {
template<typename R, class T, typename ... Args>
struct DeduceConstMemCallback {
	template<R (T::*Func)(Args...) const> inline static Callback<R(Args...)> Bind(
			T* o) {
		struct _ {
			static R wrapper(void* o, Args ... a) {
				return (static_cast<T*>(o)->*Func)(std::forward<Args>(a)...);
			}
		};
		return Callback<R(Args...)>(o, (R (*)(void*, Args...)) _::wrapper);
	}
};

template<typename R, class T, typename ... Args>
struct DeduceMemCallback {
	template<R (T::*Func)(Args...)> inline static Callback<R(Args...)> Bind(
			T* o) {
		struct _ {
			static R wrapper(void* o, Args ... a) {
				return (static_cast<T*>(o)->*Func)(std::forward<Args>(a)...);
			}
		};
		return Callback<R(Args...)>(o, (R (*)(void*, Args...)) _::wrapper);
	}
};

template<typename R, typename ... Args>
struct DeduceStaticCallback {
	template<R (*Func)(Args...)> inline static Callback<R(Args...)> Bind() {
		struct _ {
			static R wrapper(void*, Args ... a) {
				return (*Func)(std::forward<Args>(a)...);
			}
		};
		return Callback<R(Args...)>(0, (R (*)(void*, Args...)) _::wrapper);}
	};
}

template<typename R, class T, typename ... Args>
detail::DeduceConstMemCallback<R, T, Args...> DeduceCallback(R (T::*)(Args...)const) {
			return detail::DeduceConstMemCallback<R, T, Args...>();
		}

template<typename R, class T, typename ... Args>
detail::DeduceMemCallback<R, T, Args...> DeduceCallback(R(T::*)(Args...)) {
	return detail::DeduceMemCallback<R, T, Args...>();
}

template<typename R, typename ... Args>
detail::DeduceStaticCallback<R, Args...> DeduceCallback(R(*)(Args...)) {
	return detail::DeduceStaticCallback<R, Args...>();
}

template<typename ... T1> class Event {
public:
	typedef void (*TSignature)(T1...);
	typedef Callback<void(T1...)> TCallback;
	typedef std::vector<TCallback> InvocationTable;

protected:
	InvocationTable invocations;

public:
	const static int ExpectedFunctorCount = 2;

	Event() :
			invocations() {
		invocations.reserve(ExpectedFunctorCount);
	}

	template<void (*TFunc)(T1...)> void Add() {
		TCallback c = DeduceCallback(TFunc).template Bind<TFunc>();
		invocations.push_back(c);
	}

	template<typename T, void (T::*TFunc)(T1...)> void Add(T& object) {
		Add<T, TFunc>(&object);
	}

	template<typename T, void (T::*TFunc)(T1...)> void Add(T* object) {
		TCallback c = DeduceCallback(TFunc).template Bind<TFunc>(object);
		invocations.push_back(c);
	}

	template<typename T, void (T::*TFunc)(T1...) const> void Add(T& object) {
		Add<T, TFunc>(&object);
	}

	template<typename T, void (T::*TFunc)(T1...) const> void Add(T* object) {
		TCallback c = DeduceCallback(TFunc).template Bind<TFunc>(object);
		invocations.push_back(c);
	}

	void Invoke(T1 ... t1) {
		for (size_t i = 0; i < invocations.size(); ++i)
			invocations[i](std::forward<T1>(t1)...);
	}

	void operator()(T1 ... t1) {
		Invoke(std::forward<T1>(t1)...);
	}

	size_t InvocationCount() {
		return invocations.size();
	}

	template<void (*TFunc)(T1...)> bool Remove() {
		return Remove(DeduceCallback(TFunc).template Bind<TFunc>());
	}
	template<typename T, void (T::*TFunc)(T1...)> bool Remove(T& object) {
		return Remove<T, TFunc>(&object);
	}
	template<typename T, void (T::*TFunc)(T1...)> bool Remove(T* object) {
		return Remove(DeduceCallback(TFunc).template Bind<TFunc>(object));
	}
	template<typename T, void (T::*TFunc)(T1...) const> bool Remove(T& object) {
		return Remove<T, TFunc>(&object);
	}
	template<typename T, void (T::*TFunc)(T1...) const> bool Remove(T* object) {
		return Remove(DeduceCallback(TFunc).template Bind<TFunc>(object));
	}

protected:
	bool Remove(TCallback const& target) {
		auto it = std::find(invocations.begin(), invocations.end(), target);
		if (it == invocations.end())
			return false;
		invocations.erase(it);
		return true;
	}
}
;

namespace IntStatic {
void VoidTest() {
	std::cout << "INTO THE VOID" << std::endl;
}
void IntTest(int num) {
	std::cout << "Got myself a " << num << " !" << std::endl;
}
void IntTest2(int num) {
	std::cout << "Now _I_ Got myself a " << num << " !" << std::endl;
}
}

struct Int {
	void Test(int num) {
		std::cout << num << " on the inside of a class... ?" << std::endl;
	}
	void Test2(int num) {
		std::cout << num << " on the inside of a struct, yo !" << std::endl;
	}
	static void Test3(int snum) {
		std::cout << snum << " on the inside of a STATIC method?!" << std::endl;
	}
}
;

struct Multi {
	void Test(std::string woo, std::string yeah) {
		std::cout << "Dat Multi Member Function: ";
		std::cout << woo << " | " << yeah << std::endl;
	}

	void static Test2(std::string woo, std::string yeah) {
		std::cout << "Dat Static Multi Function: ";
		std::cout << woo << " | " << yeah << std::endl;
	}
}
;

int main(int argc, char* argv[]) {

	Event<int> intev;
	Int i;
	Multi m;

	intev.Add<Int, &Int::Test>(i);
	intev.Add<&IntStatic::IntTest>();
	intev.Add<&IntStatic::IntTest2>();
	intev(20);
	intev.Remove<&IntStatic::IntTest>();
	intev.Remove<&IntStatic::IntTest>();
	intev.Remove<Int, &Int::Test>(i);
	intev(20);

	Event<std::string, std::string> doublestringev;

	doublestringev.Add<Multi, &Multi::Test>(m);
	doublestringev("Bark Bark", "Meow Meow");
	doublestringev.Remove<Multi, &Multi::Test>(m);

	doublestringev.Add<&Multi::Test2>();
	doublestringev("Bahh Bahh", "Moo Moo");

	return 0;
}
