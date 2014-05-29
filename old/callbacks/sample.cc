template<typename TFuncSignature>
class Callback;

/////////////////
/* 2 ARGUMENT  */
/////////////////
template<typename R, typename T1, typename T2>
class Callback<R(T1, T2)> {
public:
	typedef R (*TFunc)(void*, T1, T2);

	const static size_t Arity = 2;

	Callback() :
			obj(0), func(0) {
	}
	Callback(void* o, TFunc f) :
			obj(o), func(f) {
	}

	R operator()(T1 t1, T2 t2) const {
		return (*func)(obj, t1, t2);
	}

	typedef void* Callback::*SafeBoolType;
	operator SafeBoolType() const {
		return func != 0 ? &Callback::obj : 0;
	}

	bool operator!() const {
		return func == 0;
	}

	bool operator==(const Callback<R(T1, T2)>& right) const {
		return obj == right.obj && func == right.func;
	}

	bool operator!=(const Callback<R(T1, T2)>& right) const {
		return obj != right.obj || func != right.func;
	}

private:
	void* obj;
	TFunc func;
};

namespace detail {
template<typename R, class T, typename T1, typename T2>
struct DeduceConstMemCallback2 {
	template<R (T::*Func)(T1, T2) const> inline static Callback<R(T1, T2)> Bind(
			T* o) {
		struct _ {
			static R wrapper(void* o, T1 t1, T2 t2) {
			return (static_cast<T*>(o)->*Func)(std::forward<T1>(t1, t2);}
			};
			return Callback<R(T1, T2)>(o, (R (*)(void*, T1, T2)) _::wrapper);
		}
	};

template<typename R, class T, typename T1, typename T2>
struct DeduceMemCallback2 {
	template<R (T::*Func)(T1, T2)> inline static Callback<R(T1, T2)> Bind(
			T* o) {
		struct _ {
			static R wrapper(void* o, T1 t1, T2 t2) {
			return (static_cast<T*>(o)->*Func)(t1, t2));}
		};
		return Callback<R(T1, T2)>(o, (R (*)(void*, T1, T2)) _::wrapper);
	}
};

template<typename R, typename T1, typename T2>
struct DeduceStaticCallback2 {
	template<R (*Func)(T1, T2)> inline static Callback<R(T1, T2)> Bind() {
		struct _ {
			static R wrapper(void*, T1 t1, T2 t2) {
			return (*Func)(t1), t2);}
		};
		return Callback<R(T1, T2)>(0, (R (*)(void*, T1, T2)) _::wrapper);}
	};
}

template<typename R, class T, typename T1, typename T2>
detail::DeduceConstMemCallback2<R, T, T1, T2> DeduceCallback2(R (T::*)(T1, T2)const) {
			return detail::DeduceConstMemCallback2<R, T, T1, T2>();
		}

template<typename R, class T, typename T1, typename T2>
detail::DeduceMemCallback2<R, T, T1, T2> DeduceCallback2(R (T::*)(T1, T2)) {
	return detail::DeduceMemCallback2<R, T, T1, T2>();
}

template<typename R, typename T1, typename T2>
detail::DeduceStaticCallback2<R, T1, T2> DeduceCallback2(R (*)(T1, T2)) {
	return detail::DeduceStaticCallback2<R, T1, T2>();
}

template<typename T1, typename T2> class Event2 {
public:
	typedef void (*TSignature)(T1, T2);
	typedef Callback<void(T1, T2)> TCallback;
	typedef std::vector<TCallback> InvocationTable;

protected:
	InvocationTable invocations;

public:
	const static int ExpectedFunctorCount = 2;

	Event2() :
			invocations() {
		invocations.reserve(ExpectedFunctorCount);
	}

	Event2(int expectedfunctorcount) :
			invocations() {
		invocations.reserve(expectedfunctorcount);
	}

	template<void (*TFunc)(T1, T2)> void Add() {
		TCallback c = DeduceCallback2(TFunc).template Bind<TFunc>();
		invocations.push_back(c);
	}

	template<typename T, void (T::*TFunc)(T1, T2)> void Add(T& object) {
		Add<T, TFunc>(&object);
	}

	template<typename T, void (T::*TFunc)(T1, T2)> void Add(T* object) {
		TCallback c = DeduceCallback2(TFunc).template Bind<TFunc>(object);
		invocations.push_back(c);
	}

	template<typename T, void (T::*TFunc)(T1, T2) const> void Add(T& object) {
		Add<T, TFunc>(&object);
	}

	template<typename T, void (T::*TFunc)(T1, T2) const> void Add(T* object) {
		TCallback c = DeduceCallback2(TFunc).template Bind<TFunc>(object);
		invocations.push_back(c);
	}

	void Invoke(T1 t1, T2 t2) {
		size_t i;
		for (i = 0; i < invocations.size(); ++i) {
			invocations[i](t1, t2);
		}
	}

	void operator()(T1 t1, T2 t2) {
		size_t i;
		for (i = 0; i < invocations.size(); ++i) {
			invocations[i](t1, t2);
		}
	}

	size_t InvocationCount() {
		return invocations.size();
	}

	template<void (*TFunc)(T1, T2)> bool Remove() {
		return Remove(DeduceCallback2(TFunc).template Bind<TFunc>());
	}
	template<typename T, void (T::*TFunc)(T1, T2)> bool Remove(T& object) {
		return Remove<T, TFunc>(&object);
	}
	template<typename T, void (T::*TFunc)(T1, T2)> bool Remove(T* object) {
		return Remove(DeduceCallback2(TFunc).template Bind<TFunc>(object));
	}
	template<typename T, void (T::*TFunc)(T1, T2) const> bool Remove(
			T& object) {
		return Remove<T, TFunc>(&object);
	}
	template<typename T, void (T::*TFunc)(T1, T2) const> bool Remove(
			T* object) {
		return Remove(DeduceCallback2(TFunc).template Bind<TFunc>(object));
	}

protected:

	bool Remove(TCallback const& target) {
		auto it = std::find(invocations.begin(), invocations.end(), target);
		if (it == invocations.end())
			return false;
		invocations.erase(it);
		return true;
	}

};
