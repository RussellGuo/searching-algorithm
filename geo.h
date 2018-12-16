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
#include <set>
#include <map>

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
    // define a point by x and y
    Point(const Rational &_x, const Rational &_y):
        x(_x), y(_y)
    {
        if (!isValid(x, y)) {
            x = y = INVALID_COORD;
        }
    }
    Point(const Point &) = default;
    Point& operator =(const Point &) = default;

    void symmetryRegular(Point &ret) const {
        ret.x = Rational(std::abs(x.numerator()), x.denominator());
        ret.y = Rational(std::abs(y.numerator()), y.denominator());
        if (ret.x < ret.y) {
            std::swap(ret.x, ret.y);
        }
    }

    void setEightSymmetry(Point symmetryArray[8]) const {
        // origin
        symmetryArray[0].x = +x;
        symmetryArray[0].y = +y;
        // mirror x-axis, x' = x, y' = -y
        symmetryArray[1].x = +x;
        symmetryArray[1].y = -y;
        // mirror y-axis x' = -x, y' = y
        symmetryArray[2].x = -x;
        symmetryArray[2].y = +y;
        // centrosymmetric to (0,0), x' = -x, y' = -y
        symmetryArray[3].x = -x;
        symmetryArray[3].y = -y;
        // swap x,y and do above again
        // origin x'= y, y' = x
        symmetryArray[4].x = +y;
        symmetryArray[4].y = +x;
        // mirror x-axis x' = y, y' = -x
        symmetryArray[5].x = +y;
        symmetryArray[5].y = -x;
        // mirror y-axis, x' = -y, y' = x
        symmetryArray[6].x = -y;
        symmetryArray[6].y = +x;
        // centrosymmetric to (0,0), x' = -y, y' = -x
        symmetryArray[7].x = -y;
        symmetryArray[7].y = -x;
    }

    // an auxilliary class for unordered set/map
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
        return std::abs(v.numerator()) <= MAX_GRID_COORD * v.denominator();
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
    Rational x, y;

};

typedef std::set<Point> PointSet;


class Line {
public:
    Line(): a(0), b(0), c(0) {} // an invalid line
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

    void setEightSymmetry(Line symmetryArray[8]) const {
        // origin
        symmetryArray[0].a = +a;
        symmetryArray[0].b = +b;
        symmetryArray[0].c = +c;
        // mirror x-axis, x' = x, y' = -y
        symmetryArray[1].a = +a;
        symmetryArray[1].b = -b;
        symmetryArray[1].c = +c;
        // mirror y-axis x' = -x, y' = y
        symmetryArray[2].a = -a;
        symmetryArray[2].b = +b;
        symmetryArray[2].c = +c;
        // centrosymmetric to (0,0), x' = -x, y' = -y
        symmetryArray[3].a = -a;
        symmetryArray[3].b = -b;
        symmetryArray[3].c = +c;
        // swap x,y and do above again
        // origin x'= y, y' = x
        symmetryArray[4].a = +b;
        symmetryArray[4].b = +a;
        symmetryArray[4].c = +c;
        // mirror x-axis x' = y, y' = -x
        symmetryArray[5].a = +b;
        symmetryArray[5].b = -a;
        symmetryArray[5].c = +c;
        // mirror y-axis, x' = -y, y' = x
        symmetryArray[6].a = -b;
        symmetryArray[6].b = +a;
        symmetryArray[6].c = +c;
        // centrosymmetric to (0,0), x' = -y, y' = -x
        symmetryArray[7].a = -b;
        symmetryArray[7].b = -a;
        symmetryArray[7].c = +c;

        for (unsigned short i = 1; i < 8; i++) {
            symmetryArray[i].sign_adjust();
        }
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

    // an auxilliary class for unordered set/map
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

        sign_adjust();
    }
    void sign_adjust() {
        if (a < 0 || (a == 0 && b < 0)) {
            a = -a;
            b = -b;
            c = -c;
        }
    }

    Int a, b, c;
};

typedef std::set<Line> LineSet;

void testGeoLine();

}

#endif // GEO_H
