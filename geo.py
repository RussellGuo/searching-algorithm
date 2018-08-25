import fractions, math


class Line: pass


class Point:
    def __init__(self, _x: fractions.Fraction, _y: fractions.Fraction):
        self.x = _x
        self.y = _y

    def __repr__(self):
        return '<%s, %s>' % (self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


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
        if a < 0 < g:  # let shadow_a be >= 0
            g = -g
        self.__shadow_a = a // g
        self.__shadow_b = b // g
        self.__shadow_c = c // g

    def contain_point(self, p: Point) -> bool:
        l = self.__shadow_a * p.x + self.__shadow_b * p.y - self.__shadow_c
        return l == 0

    def get_cross_point(self, other: Line) -> Point:
        def det2(_a, _b, _c, _d):
            return _a * _d - _b * _c

        _d = det2(self.__shadow_a, self.__shadow_b, other.__shadow_a, other.__shadow_b)
        dx = det2(self.__shadow_c, self.__shadow_b, other.__shadow_c, other.__shadow_b)
        dy = det2(self.__shadow_a, self.__shadow_c, other.__shadow_a, other.__shadow_c)
        return Point(fractions.Fraction(dx, _d), fractions.Fraction(dy, _d))

    @staticmethod
    def get_line_contains_points(p1: Point, p2: Point) -> Line:
        a = p1.y - p2.y
        b = p2.x - p1.x
        c = p2.x * p1.y - p1.x * p2.y
        line = Line(a, b, c)
        return line

    def __repr__(self):
        return '<%s * x + %s * y = %s>' % (self.a, self.b, self.c)

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
    p1 = Point(0, 0)
    p2 = Point(2, 2)
    p3 = Point(1, 1.5)
    p4 = Point(1.5, 0.5)
    l1 = Line.get_line_contains_points(p1, p2)
    l2 = Line.get_line_contains_points(p3, p4)
    l3 = Line.get_line_contains_points(p1, p2)
    print(set([l3, l1]))
    p = l1.get_cross_point(l2)
    print(p)
