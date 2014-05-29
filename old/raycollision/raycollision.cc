//#include "vector3.h"

typedef float Vector3; // placeholder

enum eBlockType{
    None = 0,
    One, 
    Two, 
    Three
};

static int searchGranularity = 0;

eBlockType BlockAtPoint(const Vector3 testPos)
{
  eBlockType b;
  return b;
}

bool RayCollision(const Vector3& startPosition, const Vector3& rayDirection, const float& distance, const int& searchGranularity, Vector3& hitPoint, Vector3& buildPoint)
{
  Vector3 testPos  = startPosition;
  Vector3 buildPos = startPosition;

  for (int i=0; i < searchGranularity; i++)
  {
    testPos += rayDirection * distance / searchGranularity;
    eBlockType testBlock = BlockAtPoint(testPos);
    if (testBlock != None)
    {
      hitPoint   = testPos;
      buildPoint = buildPos;
      return true;
    }
    buildPos = testPos;
  }

  return false;
}
