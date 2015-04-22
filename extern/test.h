/* Header file foo.h */
#ifdef __cplusplus /* If this is a C++ compiler, use C linkage */
extern "C" {
#endif
   
  /* These functions get C linkage */
  void foo();
   
  struct bar { /* ... */ };
   
#ifdef __cplusplus /* If this is a C++ compiler, end C linkage */
}
#endif
