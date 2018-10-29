#ifndef GEO_H
#define GEO_H

#include <boost/rational.hpp>

namespace geo {

class TLine;
class TPoint;

typedef int32_t TInt;
typedef boost::rational<TInt> TRational;


class TPoint {
public:
    // define a point by x and y
    TPoint(const TRational &_x, const TRational &_y):
        x(_x), y(_y)
    {
    }
    // define a point by 2 lines' intersection
    TPoint(const TLine &Line1, const TLine &Line2);

    TRational getX() const
    {
        return x;
    }

    TRational getY() const
    {
        return y;
    }

private:
    const TRational x,y;
};

class TLine {
public:
    // ax + by = c, define a line by a, b and c
    TLine(const TRational &_a, const TRational &_b, const TRational &_c):
        a(_a), b(_b), c(_c) {

    }
    // define a line by 2 collinear points
    TLine (const TPoint&p1,  const TPoint&p2);
private:
    const TRational a, b, c;
};

}

#endif // GEO_H
