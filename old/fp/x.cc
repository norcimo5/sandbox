#ifndef FASTDELEGATE_H
#define FASTDELEGATE_H

#include <cstring>
#include <type_traits>
#include <cassert>
#include <cstddef>
#include <memory>
#include <new>
#include <utility>

namespace ssvu
{
    namespace detail
        {
              class AnyClass;
                  constexpr std::size_t SingleMemFuncPtrSize{sizeof(void(AnyClass::*)())};

                      template<class TOut, class TIn> union HorribleUnion { TOut out; TIn in; };
                          template<class TOut, class TIn> inline TOut implicit_cast(TIn mIn) noexcept { return mIn; }
                              template<class TOut, class TIn> inline TOut horrible_cast(TIn mIn) noexcept
                                    {
                                            HorribleUnion<TOut, TIn> u;
                                                  static_assert(sizeof(TIn) == sizeof(u) && sizeof(TIn) == sizeof(TOut), "Cannot use horrible_cast<>");
                                                        u.in = mIn; return u.out;
                                                            }
                                  template<class TOut, class TIn> inline TOut unsafe_horrible_cast(TIn mIn) noexcept { HorribleUnion<TOut, TIn> u; u.in = mIn; return u.out; }

                                      template<std::size_t N> struct SimplifyMemFunc
                                            {
                                                    template<class X, class XFuncType, class AnyMemFunc> inline static AnyClass* convert(const X*, XFuncType, AnyMemFunc&) noexcept
                                                            {
                                                                      static_assert(N - 100, "Unsupported member function pointer on this compiler");
                                                                              return 0;
                                                                                    }
                                                        };
                                          template<> struct SimplifyMemFunc<SingleMemFuncPtrSize>
                                                {
                                                        template<class X, class XFuncType, class AnyMemFunc> inline static AnyClass* convert(const X* pthis, XFuncType function_to_bind, AnyMemFunc& bound_func) noexcept
                                                                {
                                                                          bound_func = reinterpret_cast<AnyMemFunc>(function_to_bind);
                                                                                  return reinterpret_cast<AnyClass*>(const_cast<X*>(pthis));
                                                                                        }
                                                            };
                                            }

      class DelegateMemento
          {
                protected:
                        using AnyMemFunc = void(detail::AnyClass::*)();

                              detail::AnyClass* ptrThis;
                                    AnyMemFunc ptrFunction;

                                          inline void setFrom(const DelegateMemento& mMemento) noexcept { ptrFunction = mMemento.ptrFunction; ptrThis = mMemento.ptrThis; }

                                              public:
                                                inline DelegateMemento() : ptrThis{nullptr}, ptrFunction{nullptr} { }
                                                      inline DelegateMemento(const DelegateMemento& mMemento) : ptrThis{mMemento.ptrThis}, ptrFunction{mMemento.ptrFunction} { }

                                                            inline DelegateMemento& operator=(const DelegateMemento& mMemento) noexcept { setFrom(mMemento); return *this; }
                                                                  inline void clear() noexcept { ptrThis = nullptr; ptrFunction = nullptr; }

                                                                        inline bool isEqual(const DelegateMemento& mMemento) const noexcept { return ptrThis == mMemento.ptrThis && ptrFunction == mMemento.ptrFunction; }
                                                                              inline bool isLess(const DelegateMemento& mMemento) const     { return ptrThis != mMemento.ptrThis ? ptrThis < mMemento.ptrThis : std::memcmp(&ptrFunction, &mMemento.ptrFunction, sizeof(ptrFunction)) < 0; }
                                                                                    inline std::size_t getHash() const                  { return reinterpret_cast<std::size_t>(ptrThis) ^ detail::unsafe_horrible_cast<size_t>(ptrFunction); }

                                                                                          inline bool isEmpty() const noexcept              { return ptrThis == nullptr && ptrFunction == nullptr; }
                                                                                                inline bool operator<(const DelegateMemento& mMemento) const  { return isLess(mMemento); }
                                                                                                      inline bool operator>(const DelegateMemento& mMemento) const  { return mMemento.isLess(*this); }
                                                                                                        };

        namespace detail
            {
                  template<class TAnyMemFunc, class TStaticFunc, class TUnvoidStaticFunc> struct ClosurePtr : public DelegateMemento
                                                                                                                  {
                                                                                                                          inline void copyFrom(const DelegateMemento& mMemento) { setFrom(mMemento); }

                                                                                                                                template<class X, class XMemFunc> inline void bindMemFunc(X* mPtrThis, XMemFunc mFuncToBind) { ptrThis = SimplifyMemFunc<sizeof(mFuncToBind)>::convert(mPtrThis, mFuncToBind, ptrFunction); }
                                                                                                                                      template<class DerivedClass, class ParentInvokerSig> inline void bindStaticFunc(DerivedClass* mPtrParent, ParentInvokerSig mStaticFuncInvoker, TStaticFunc mFuncToBind)
                                                                                                                                              {
                                                                                                                                                        if(mFuncToBind == nullptr) ptrFunction = nullptr; else bindMemFunc(mPtrParent, mStaticFuncInvoker);
                                                                                                                                                                static_assert(sizeof(AnyClass*) == sizeof(mFuncToBind), "Cannot use evil method");
                                                                                                                                                                        ptrThis = horrible_cast<AnyClass*>(mFuncToBind);
                                                                                                                                                                              }

                                                                                                                                            inline AnyClass* getPtrThis() const noexcept            { return ptrThis; }
                                                                                                                                                  inline TAnyMemFunc getPtrFunction() const noexcept          { return reinterpret_cast<TAnyMemFunc>(ptrFunction); }
                                                                                                                                                        inline TUnvoidStaticFunc getStaticFunc() const noexcept       { static_assert(sizeof(TUnvoidStaticFunc) == sizeof(this), "Cannot use evil method"); return horrible_cast<TUnvoidStaticFunc>(this); }
                                                                                                                                                              inline bool isEqualToStaticFuncPtr(TStaticFunc mPtr) const noexcept { return mPtr == nullptr ? isEmpty() : mPtr == reinterpret_cast<TStaticFunc>(getStaticFunc()); }
                                                                                                                                                                  };
                    }

          template<typename TReturn, typename... TArgs> class FastFuncImpl
              {
                    private:
                            inline TReturn invokeStaticFunc(TArgs... mArgs) const { return (*(closure.getStaticFunc()))(mArgs...); }

                                protected:
                                  template<typename X> using XFuncToBind = TReturn(X::*)(TArgs...) const;
                                        using FuncSig = TReturn(*)(TArgs...);
                                              using GenericMemFn = TReturn(detail::AnyClass::*)(TArgs...);
                                                    using ClosureType = detail::ClosurePtr<GenericMemFn, FuncSig, FuncSig>;
                                                          ClosureType closure;

                                                              public:
                                                                inline FastFuncImpl() noexcept { clear(); }
                                                                      inline FastFuncImpl(std::nullptr_t) noexcept { clear(); }
                                                                            inline FastFuncImpl(const FastFuncImpl& mImpl) { closure.copyFrom(mImpl.closure); }
                                                                                  inline FastFuncImpl(FuncSig mFuncToBind) { bind(mFuncToBind); }
                                                                                        template<typename X, typename Y> inline FastFuncImpl(Y* mPtrThis, XFuncToBind<X> mFuncToBind) { bind(mPtrThis, mFuncToBind); }

                                                                                              inline void clear() { closure.clear();}
                                                                                                    inline void operator=(const FastFuncImpl& mImpl) { closure.copyFrom(mImpl.closure); }
                                                                                                          inline void operator=(const FuncSig mFuncToBind) { bind(mFuncToBind); }
                                                                                                                inline TReturn operator()(TArgs... mArgs) const { return (closure.getPtrThis()->*(closure.getPtrFunction()))(mArgs...); }

                                                                                                                      inline bool operator==(const FastFuncImpl& mImpl) const noexcept  { return closure.isEqual(mImpl.closure); }
                                                                                                                            inline bool operator==(FuncSig mFuncPtr) const noexcept       { return closure.isEqualToStaticFuncPtr(mFuncPtr); }
                                                                                                                                  inline bool operator==(std::nullptr_t) const noexcept       { return closure.isEmpty(); }
                                                                                                                                        inline bool operator!=(const FastFuncImpl& mImpl) const noexcept  { return !this->operator==(mImpl); }
                                                                                                                                              inline bool operator!=(FuncSig mFuncPtr) const noexcept       { return !this->operator==(mFuncPtr); }
                                                                                                                                                    inline bool operator!=(std::nullptr_t) const noexcept       { return !this->operator==(nullptr); }
                                                                                                                                                          inline bool operator<(const FastFuncImpl& mImpl) const        { return closure.isLess(mImpl.closure); }
                                                                                                                                                                inline bool operator>(const FastFuncImpl& mImpl) const        { return mImpl.closure.isLess(closure); }

                                                                                                                                                                      inline void bind(const FuncSig mFuncToBind) { closure.bindStaticFunc(this, &FastFuncImpl::invokeStaticFunc, mFuncToBind); }
                                                                                                                                                                            template<typename X, typename Y> inline void bind(Y* mPtrThis, XFuncToBind<X> mFuncToBind) { closure.bindMemFunc(detail::implicit_cast<const X*>(mPtrThis), mFuncToBind); }
                                                                                                                                                                              };

            template<typename TSignature> class FastFunc;
              template<typename TReturn, typename... TArgs> class FastFunc<TReturn(TArgs...)> : public FastFuncImpl<TReturn, TArgs...>
                  {
                        private:
                                std::shared_ptr<void> storage;
                                      template<typename T> inline static void FuncDeleter(void* const mPtr) { static_cast<T*>(mPtr)->~T(); operator delete(mPtr); }

                                          public:
                                            using BaseType = FastFuncImpl<TReturn, TArgs...>;
                                                  using BaseType::BaseType;

                                                        inline FastFunc() = default;
                                                              template<typename TFunc, typename = typename ::std::enable_if<!::std::is_same<FastFunc, typename ::std::decay<TFunc>::type>{}>::type> FastFunc(TFunc&& mFunc)
                                                                        : storage(operator new(sizeof(TFunc)), FuncDeleter<typename ::std::decay<TFunc>::type>)
                                                                              {
                                                                                        using FuncType = typename ::std::decay<TFunc>::type;
                                                                                                new (storage.get()) FuncType(::std::forward<TFunc>(mFunc));
                                                                                                        this->closure.bindMemFunc(storage.get(), &FuncType::operator());
                                                                                                              }
                                                                };
}

#endif
