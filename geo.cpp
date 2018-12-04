#include "geo.h"

using namespace geo;

void geo::testGeoLine()
{
    Line line1(0, 1, Rational(1,2));
    Line line2(1, 0, Rational(1,2));
    Point p(Line::getIntersectionPoint(line1,line2));
    p.isValid();
}
