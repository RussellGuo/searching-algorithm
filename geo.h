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
inline size_t hashValue(const Rational &v)
{
    size_t ret;
    ret = hashValue(v.numerator()) | (hashValue(v.denominator()) << 16);
    return ret;
}


constexpr Int MAX_GRID_COORD = 3;
constexpr Int INVALID_COORD = -MAX_GRID_COORD - 1;

inline Int det2(Int a, Int b, Int c, Int d)
{
    auto ret = a * d - b * c;
    return ret;
}


class Point {
public:
    explicit Point():x(INVALID_COORD), y(INVALID_COORD) {}
    Point(const Rational &_x, const Rational &_y):
        x(_x), y(_y)
    {
        if (!isValid(x, y)) {
            x = y = INVALID_COORD;
        }
    }
    Point(const Point &) = default;
    Point& operator =(const Point &) = default;

    // a auxilliary class for unordered set/map
    struct hash {
        size_t operator()(const Point& p) const
        {
            return size_t(p.x.numerator()) | size_t((p.x.denominator()) << 8) | size_t((p.y.numerator()) << 16) | size_t((p.y.denominator()) << 24);
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

    static bool isValid(const Rational &v) {
        return abs(v.numerator()) <= MAX_GRID_COORD * v.denominator();
    }
    static bool isValid(const Rational &x, const Rational &y) {
        return isValid(x) && isValid(y);
    }
    Rational getY() const
    {
        return y;
    }

    Rational getX() const
    {
        return x;
    }

private:
    // define a point by x and y
    Rational x, y;

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
        auto _a = p1.getY() - p2.getY();
        auto _b = p2.getX() - p1.getX();
        auto _c = p2.getX() * p1.getY() - p1.getX() * p2.getY();
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
    bool operator != (const Line &other) const {
        return !(*this == other);
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
    static bool getIntersectionPoint(const Line &Line1, const Line &Line2, Point &point)
    {
        auto det = det2(Line1.a, Line1.b, Line2.a, Line2.b);
        if (det == 0) {
            return false;
        }
        auto dx = det2(Line1.c, Line1.b, Line2.c, Line2.b);
        auto dy = det2(Line1.a, Line1.c, Line2.a, Line2.c);
        auto x = Rational(dx, det);
        auto y = Rational(dy, det);
        point = Point(x, y);
        return point.isValid();
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
