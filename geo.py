import fractions, math


class Line: pass


class Point:
    def __init__(self, x: fractions.Fraction, y: fractions.Fraction):
        self.x = x
        self.y = y

    def __repr__(self):
        return '<%s, %s>' % (self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.y, self.x) == (other.y, other.x)

    def __ne__(self, other):
        return (self.y, self.x) != (other.y, other.x)

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def __le__(self, other):
        return (self.y, self.x) <= (other.y, other.x)

    def __gt__(self, other):
        return (self.y, self.x) > (other.y, other.x)

    def __ge__(self, other):
        return (self.y, self.x) >= (other.y, other.x)


class Line:
    def __init__(self, _a: fractions.Fraction, _b: fractions.Fraction, _c: fractions.Fraction):
        self.a = fractions.Fraction(_a)
        self.b = fractions.Fraction(_b)
        self.c = fractions.Fraction(_c)

        # try to normalize it
        denominator = self.a.denominator * self.b.denominator * self.c.denominator

        a = (self.a * denominator).numerator
        b = (self.b * denominator).numerator
        c = (self.c * denominator).numerator
        g = math.gcd(a, b)
        g: int = math.gcd(g, c)
        self.__shadow_a = a // g
        self.__shadow_b = b // g
        self.__shadow_c = c // g
        if self.__shadow_a < 0 or self.__shadow_a == 0 and self.__shadow_b < 0:
            self.__shadow_a *= -1
            self.__shadow_b *= -1
            self.__shadow_a *= -1

    def contain_point(self, p: Point) -> bool:
        l = self.__shadow_a * p.x + self.__shadow_b * p.y - self.__shadow_c
        return l == 0

    def get_cross_point(self, other: Line, new_point_checker=None) -> Point:
        def det2(_a, _b, _c, _d):
            return _a * _d - _b * _c

        _d = det2(self.__shadow_a, self.__shadow_b, other.__shadow_a, other.__shadow_b)
        if _d == 0:
            return None

        dx = det2(self.__shadow_c, self.__shadow_b, other.__shadow_c, other.__shadow_b)
        dy = det2(self.__shadow_a, self.__shadow_c, other.__shadow_a, other.__shadow_c)
        x, y = fractions.Fraction(dx, _d), fractions.Fraction(dy, _d)
        if new_point_checker and not new_point_checker(x, y):
            return None
        return Point(x, y)

    @staticmethod
    def get_line_contains_points(p1: Point, p2: Point) -> Line:
        if p1 == p2:
            return None
        a = p1.y - p2.y
        b = p2.x - p1.x
        c = p2.x * p1.y - p1.x * p2.y
        line = Line(a, b, c)
        return line

    def __repr__(self):
        return '<%s * x + %s * y = %s>' % (self.__shadow_a, self.__shadow_b, self.__shadow_c)

    def __hash__(self):
        return hash((self.__shadow_a, self.__shadow_b, self.__shadow_c))

    def __eq__(self, other: Line):
        return self.__shadow_a == other.__shadow_a and self.__shadow_b == other.__shadow_b and self.__shadow_c == other.__shadow_c


if __name__ == "__main__":
    half = fractions.Fraction(0.5)

    a = half + half * 3 + half * 3
    x1 = a / 3

    b = half + half + half * 3
    x2 = b / 3

    x3 = x4 = x2 + 4
    print((x1 + x2 + x3 + x4) / 4)
    test_p1 = Point(0, 0)
    test_p2 = Point(2, 2)
    test_p3 = Point(1, 1.5)
    test_p4 = Point(1.5, 0.5)
    test_l1 = Line.get_line_contains_points(test_p1, test_p2)
    test_l2 = Line.get_line_contains_points(test_p3, test_p4)
    test_l3 = Line.get_line_contains_points(test_p1, test_p2)
    print({test_l3, test_l1})
    p = test_l1.get_cross_point(test_l2)
    print(p)
    print(test_l1.get_cross_point(test_l1))
