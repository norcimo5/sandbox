Sine<N,I>:
  x * SineSeries<N,I,10,0>
  SineSeries<N,I,J,K>:
    1-x*x/(2*K+2)/(2*K+3) *  SineSeries<N*go, I*go,J*go, (K+1)*go>
    SineSeries<0,0,0,0>:
      1;

template<int N, int I>
class Sine {
  public:
        static inline float sin()
              {
                        return (I*2*M_PI/N) * SineSeries<N,I,10,0>::accumulate();
                            }
};


// Compute J terms in the series expansion.  K is the loop variable.
template<int N, int I, int J, int K>
class SineSeries {
  public:
        enum { go = (K+1 != J) };

            static inline float accumulate()
                  {
                            return 1-(I*2*M_PI/N)*(I*2*M_PI/N)/(2*K+2)/(2*K+3) *
                                          SineSeries<N*go,I*go,J*go,(K+1)*go>::accumulate();
                                }
};


// Specialization to terminate loop
class SineSeries<0,0,0,0> {
  public:
        static inline float accumulate()
              { return 1; }
};
