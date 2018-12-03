#ifndef GEO_H
#define GEO_H

#include <boost/rational.hpp>
#include <boost/math/common_factor.hpp>
#include <boost/integer_traits.hpp>
#include <functional>
#include <limits>
#include <algorithm>

namespace geo {

class Line;
class Point;
class Figure;

typedef int32_t Int;
inline size_t hash_value(Int v)
{
    size_t ret;
    ret = std::hash<Int>{}(v);
    return ret;
}

typedef boost::rational<Int> Rational;
inline size_t hash_value(Rational v)
{
    size_t ret;
    ret = hash_value(v.numerator()) | (hash_value(v.denominator()) << 16);
    return ret;
}

const Rational MAX_GRID_COORD = 3;

inline Int Det2(Int a, Int b, Int c, Int d)
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
    static Point GetInvalidPoint() {
        auto min = std::numeric_limits<Int>::min();
        return Point(min, min);
    }

    Point(const Point &) = default;
    Point& operator =(const Point &) = delete;
    const Rational x, y;

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

    struct Hash {
        size_t operator()(Point const& p) const
        {
            std::size_t hx = hash_value(p.x);
            std::size_t hy = hash_value(p.y);
            return hx | (hy << 8);
        }
    };

    bool IsValid() const {
        return IsValid(x, y);
    }

    static bool IsValid(const Rational &x, const Rational &y) {
        auto invalid = x < -MAX_GRID_COORD || x > MAX_GRID_COORD || y < -MAX_GRID_COORD || y > MAX_GRID_COORD;
        return !invalid;

    }

    static Point GetPoint(const Rational &x, const Rational &y) {
        if (IsValid(x, y)) {
            return Point(x, y);
        } else {
            return GetInvalidPoint();
        }
    }

};


class Line {
public:
private:
    // ax + by = c, define a line by a, b and c. They are normalized
    Line(const Int &_a, const Int &_b, const Int &_c): a(_a), b(_b), c(_c) {}
    Int a, b, c;


public:

    bool IsValid() const {
        auto ret = a > 0 || (a == 0 && b > 0);
        return ret;
    }

    void get_abc(Int &a, Int &b, Int &c) const {
        a = this->a;
        b = this->b;
        c = this->c;
    }

    static Line GetInvalidLine() {
        return Line(0, 0, 0);
    }

    struct Hash {
        size_t operator()(Line const& ll) const
        {
            std::size_t a = hash_value(ll.a);
            std::size_t b = hash_value(ll.b);
            std::size_t c = hash_value(ll.c);
            return a | (b << 8) | (c << 16);
        }
    };

    bool operator == (const Line &other) const {
        return a == other.a && b == other.b && c == other.c;
    }

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

    // define a line by 2 collinear points
    static Line GetLine(const Point&p1,  const Point&p2) {
        if (p1 == p2) {
            return GetInvalidLine();
        }
        auto a = p1.y - p2.y;
        auto b = p2.x - p1.x;
        auto c = p2.x * p1.y - p1.x * p2.y;
        auto line = GetLine(a, b, c);
        return line;

    }
    // ax + by = c, define a line by a, b and c
    static Line GetLine(const Rational &a, const Rational &b, const Rational &c) {
        Int denominator = a.denominator() * b.denominator() * c.denominator();
        Int _a = (a * denominator).numerator(), _b = (b * denominator).numerator(), _c = (c * denominator).numerator();

        if (_a == 0 && _b == 0) {
            return GetInvalidLine();
        }

        Int _gcd = boost::gcd(_a, _b);
        _gcd = boost::gcd(_gcd, _c);
        _a /= _gcd;
        _b /= _gcd;
        _c /= _gcd;
        if (_a < 0 || (_a == 0 && _b < 0)) {
            _a = -_a;
            _b = -_b;
            _c = -_c;
        }
        return Line(_a, _b, _c);
    }
    // define a point by 2 lines' intersection
    static Point GetPoint(const Line &Line1, const Line &Line2);
};

// define a point by 2 lines' intersection
inline Point Line::GetPoint(const Line &Line1, const Line &Line2)
{
    auto det = Det2(Line1.a, Line1.b, Line2.a, Line2.b);
    if (det == 0) {
        return Point::GetInvalidPoint();
    }
    auto dx = Det2(Line1.c, Line1.b, Line2.c, Line2.b);
    auto dy = Det2(Line1.a, Line1.c, Line2.a, Line2.c);
    auto x = Rational(dx, det);
    auto y = Rational(dy, det);
    auto ret = Point::GetPoint(x, y);
    return ret;
}

}

#endif // GEO_H
