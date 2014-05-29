// class Integer v.90
// Copyright Cap'n Code (C) 2004 
// "Use this without giving me credit and I'll sue!"
#pragma once
#include <iostream>

class Integer
{

public:
  typedef unsigned    __int32 Unit;
  static const unsigned MaxSize = 32;

protected:
  // Number of units that store data
  unsigned    UnitLen;

  // If > 0, (SigBit - 1) is the offset of the highest set bit
  // If < 0, (-SigBit - 2) is the offset of the highest set bit,
  // or is -1 for Integer(-1)
  // Otherwise, Integer(0)
  signed    SigBit;

  // Actual data
  Unit Data[MaxSize];

public:
  Integer(void);
  Integer(const Integer &);
  Integer(const Unit *, unsigned Count);
  Integer(const char *, unsigned Radix);
  Integer(const __wchar_t *, unsigned Radix);
  explicit Integer(signed long);

  void Not();    // 1's completement
  void Neg(); // 2's completement
  bool ShiftLeft();
  bool ShiftRight();
  
  long GetLong() const;
  void Copy(const Unit *, unsigned Count);
  void FromString(const char *, unsigned Radix);
  void FromString(const __wchar_t *, unsigned Radix);
  void MoveTo(Integer &);    // Moves data and clears this
  void ToString(char *, unsigned Radix) const;
  void ToString(__wchar_t *, unsigned Radix) const;
  
  unsigned GetUnitLength() const;
  unsigned GetSigUnitLen() const;
  Unit GetUnit(unsigned) const;
  bool GetBit(unsigned) const;
  
  bool IsZero() const;
  bool IsNegative() const;
  bool IsPositive() const;
  bool IsEven() const;
  
  Integer & operator = (signed long);
  Integer & operator = (const Integer &);
  
  bool operator == (const Integer &) const;
  bool operator != (const Integer &) const;
  bool operator <  (const Integer &) const;
  bool operator >  (const Integer &) const;
  bool operator <= (const Integer &) const;
  bool operator >= (const Integer &) const;
  
  static int Compare(const Integer &, const Integer &);
  static void Add(const Integer &, const Integer &, Integer &);
  static void Sub(const Integer &, const Integer &, Integer &);
  static void Mul(const Integer &, const Integer &, Integer &); 
  static void Div(const Integer &, const Integer &, Integer & Quo, Integer & Rem);
  static void Mod(const Integer &, const Integer &, Integer &);
  static void Exp(const Integer &, const Integer &, Integer &);
  // Computes A ^ B mod C
  static void ExpMod(const Integer &, const Integer &, 
  const Integer &, Integer &);

protected:
  void _Alloc(unsigned);
  void _ReAlloc(unsigned);
  void _DataShiftLeft(unsigned);
  bool _IsMax() const;
  bool _IsMin() const;
  void _FixSigBit();
  
  friend std::ostream & operator << (std::ostream & Str, 
  const Integer & Int);

};


