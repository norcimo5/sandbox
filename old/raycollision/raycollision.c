// C version
//#include "vector3.h"

typedef float Vector3; // placeholder

typedef enum {
    BLOCKTYPE_NONE = 0,
    BLOCKTYPE_ONE, 
    BLOCKTYPE_TWO, 
    BLOCKTYPE_THREE
} eBlockType;


eBlockType BlockAtPoint(const Vector3 testPos)
{
  eBlockType b;
  return b;
}

int RayCollision(const Vector3 startPosition, const Vector3 rayDirection, const float distance, const int searchGranularity, Vector3 * hitPoint, Vector3 * buildPoint)
{
  Vector3 testPos  = startPosition;
  Vector3 buildPos = startPosition;
  int i;

  for (i=0; i < searchGranularity; i++)
  {
    testPos += rayDirection * distance / searchGranularity;
    eBlockType testBlock = BlockAtPoint(testPos);
    if (testBlock != BLOCKTYPE_NONE)
    {
      *hitPoint   = testPos;
      *buildPoint = buildPos;
      return 0;
    }
    buildPos = testPos;
  }

  return 1;
}
