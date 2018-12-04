#ifndef GEO_H
#define GEO_H

#include <boost/rational.hpp>
#include <boost/math/common_factor.hpp>
#include <boost/integer_traits.hpp>
#include <functional>
#include <limits>
#include <algorithm>
#include <tuple>
#include <unordered_map>
#include <unordered_set>

namespace geo {

class Line;
class Point;
class Figure;


typedef int32_t Int;
inline size_t hashValue(Int v)
{
    size_t ret;
    ret = std::hash<Int>{}(v);
    return ret;
}


typedef boost::rational<Int> Rational;
inline size_t hashValue(Rational v)
{
    size_t ret;
    ret = hashValue(v.numerator()) | (hashValue(v.denominator()) << 16);
    return ret;
}


const Rational MAX_GRID_COORD = 3;

inline Int det2(Int a, Int b, Int c, Int d)
{
    auto ret = a * d - b * c;
    return ret;
}


class Point {
private:
    // define a point by x and y
    Point(const Rational &_x, const Rational &_y):
        x(_x), y(_y)
    {
    }
public:
    static Point getInvalidPoint() {
        auto min = std::numeric_limits<Int>::min();
        return Point(min, min);
    }

    Point(const Point &) = default;
    Point& operator =(const Point &) = delete;
    const Rational x, y;

    // a auxilliary class for unordered set/map
    struct hash {
        size_t operator()(const Point& p) const
        {
            std::size_t hx = hashValue(p.x);
            std::size_t hy = hashValue(p.y);
            return hx | (hy << 8);
        }
    };

    bool operator == (const Point &other) const {
        return x == other.x && y == other.y;
    }

    bool operator < (const Point &other) const {
        if (y == other.y) {
            return x < other.x;
        } else {
            return y < other.y;
        }
    }

    bool isValid() const {
        return isValid(x, y);
    }

    static bool isValid(const Rational &x, const Rational &y) {
        auto invalid = x < -MAX_GRID_COORD || x > MAX_GRID_COORD || y < -MAX_GRID_COORD || y > MAX_GRID_COORD;
        return !invalid;

    }

    static Point getPoint(const Rational &x, const Rational &y) {
        if (isValid(x, y)) {
            return Point(x, y);
        } else {
            return getInvalidPoint();
        }
    }

};

typedef std::unordered_set<Point, Point::hash> PointSet;


class Line {
public:
    // ax + by = c, define a line by a, b and c
    Line(const Rational &_a, const Rational &_b, const Rational &_c) {
        construct(_a, _b, _c);
    }

    // define a line by 2 point on it.
    Line(const Point &p1, const Point &p2) {
        auto _a = p1.y - p2.y;
        auto _b = p2.x - p1.x;
        auto _c = p2.x * p1.y - p1.x * p2.y;
        construct(_a, _b, _c);
    }

    bool isValid() const {
        auto ret = a > 0 || (a == 0 && b > 0);
        return ret;
    }

    void getParams(Int &_a, Int &_b, Int &_c) const {
        _a = a;
        _b = b;
        _c = c;
    }

    // a auxilliary class for unordered set/map
    struct hash {
        size_t operator()(const Line& ll) const
        {
            std::size_t a = hashValue(ll.a);
            std::size_t b = hashValue(ll.b);
            std::size_t c = hashValue(ll.c);
            return a | (b << 8) | (c << 16);
        }
    };

    bool operator == (const Line &other) const {
        return a == other.a && b == other.b && c == other.c;
    }

    // dictionary order, for sorting a set of lines. then set can be stored as a sorted vector,
    // the equality of two set is the one of those vectors.
    bool operator < (const Line &other) const {
        if (a < other.a) {
            return true;
        } else if (a > other.a) {
            return false;
        }

        if (b < other.b) {
            return true;
        } else if (b > other.b) {
            return false;
        }
        return c < other.c;
    }

    // get the point by 2 lines' intersection
    static Point getIntersectionPoint(const Line &Line1, const Line &Line2)
    {
        auto det = det2(Line1.a, Line1.b, Line2.a, Line2.b);
        if (det == 0) {
            return Point::getInvalidPoint();
        }
        auto dx = det2(Line1.c, Line1.b, Line2.c, Line2.b);
        auto dy = det2(Line1.a, Line1.c, Line2.a, Line2.c);
        auto x = Rational(dx, det);
        auto y = Rational(dy, det);
        auto ret = Point::getPoint(x, y);
        return ret;
    }

private:
    // ax + by = c, define a line by a, b and c. the ratioal type will be converted into int.
    void construct(const Rational &_a, const Rational &_b, const Rational &_c) {
        Int denominator = _a.denominator() * _b.denominator() * _c.denominator();
        a = (_a * denominator).numerator();
        b = (_b * denominator).numerator();
        c = (_c * denominator).numerator();

        if (a == 0 && b == 0) {
            c = 0;
            return;
        }

        Int _gcd = boost::gcd(a, b);
        _gcd = boost::gcd(_gcd, c);
        a /= _gcd;
        b /= _gcd;
        c /= _gcd;
        if (a < 0 || (a == 0 && b < 0)) {
            a = -a;
            b = -b;
            c = -c;
        }
    }

    Int a, b, c;
};

typedef std::unordered_set<Line, Line::hash> LineSet;

void testGeoLine();

}

#endif // GEO_H
