#ifndef _VECTOR2_H_
#define _VECTOR2_H_

// TODO Homework: Make this more robust, dynamic, yet simple
class Vector2 {

    public :
        Vector2(float& x, float& y) :
            m_x(x),
            m_y(y),
            m_magnitude(1.0f)
        {
        }

        // missing copy constructor

        virtual ~Vector2(){}
       
        // Todo: Add proper operators 
        Vector2& operator +(Vector2& a) { return a; }
        Vector2& operator -(Vector2& a) { return a; }
        Vector2& operator *(Vector2& a) { return a; }
        Vector2& operator /(Vector2& a) { return a; }

        void setMag(float& m) {  m_magnitude = m;}
        float getMag() { return m_magnitude; }
        // missing vector manipulation methods

    private:
        float m_x;
        float m_y;
        float m_magnitude;
        // missing more subtle but important attributes
};

#endif
