import math
from fractions import Fraction


class Point:
    def __init__(self, x: Fraction, y: Fraction, obj_tuple=None):
        self.x = x
        self.y = y
        self.obj_tuple = obj_tuple
        self.hash = None

    def __repr__(self):
        if isinstance(self.obj_tuple, str):
            return self.obj_tuple
        return '<%s, %s>' % (self.x, self.y)

    def __hash__(self):
        if self.hash is None:
            self.hash = hash((self.x, self.y))
        return self.hash

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

    def details(self):
        if self.obj_tuple is None:
            return str(self)
        if isinstance(self.obj_tuple, str):
            return self.obj_tuple
        else:
            return "%s(%s,%s)" % (self.obj_tuple[0], self.obj_tuple[1].details(), self.obj_tuple[2].details())

    def middle(self, other):
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2, ("-", self, other))

    def l2(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2


class Line:
    def __init__(self, _a: Fraction, _b: Fraction, _c: Fraction, obj_tuple=None):
        self.obj_tuple = obj_tuple

        # try to normalize it
        denominator = _a.denominator * _b.denominator * _c.denominator

        a = (_a * denominator).numerator
        b = (_b * denominator).numerator
        c = (_c * denominator).numerator
        g = math.gcd(a, b)
        g: int = math.gcd(g, c)
        self.a = a // g
        self.b = b // g
        self.c = c // g
        if self.a < 0 or self.a == 0 and self.b < 0:
            self.a *= -1
            self.b *= -1
            self.c *= -1

        self.hash = None

    def contain_point(self, p: Point) -> bool:
        l = self.a * p.x + self.b * p.y - self.c
        return l == 0

    def get_cross_point(self, other, new_point_checker=None):
        def det2(_a, _b, _c, _d):
            return _a * _d - _b * _c

        _d = det2(self.a, self.b, other.a, other.b)
        if _d == 0:
            return None

        dx = det2(self.c, self.b, other.c, other.b)
        dy = det2(self.a, self.c, other.a, other.c)
        x, y = Fraction(dx, _d), Fraction(dy, _d)
        if new_point_checker and not new_point_checker(x, y):
            return None
        return Point(x, y, ("X", self, other))

    @staticmethod
    def get_line_contains_points(p1: Point, p2: Point):
        if p1 == p2:
            return None
        a = p1.y - p2.y
        b = p2.x - p1.x
        c = p2.x * p1.y - p1.x * p2.y
        line = Line(a, b, c, ("<>", p1, p2))
        return line

    @staticmethod
    def get_line_parallel_to(other, p: Point):
        if other is None or p is None:
            return None
        a = other.a
        b = other.b
        c = a * p.x + b * p.y
        line = Line(a, b, c, ("//", other, p))
        return line

    @staticmethod
    def get_line_perpendicular_to(other, p: Point):
        if other is None or p is None:
            return None
        a = other.b
        b = -other.a
        c = a * p.x + b * p.y
        line = Line(a, b, c, ("-|", other, p))
        return line

    @staticmethod
    def get_bisectors_for_2lines(line1, line2):
        a1, b1, c1 = line1.a, line1.b, line1.c
        a2, b2, c2 = line2.a, line2.b, line2.c
        l1 = a1 ** 2 + b1 ** 2
        l2 = a2 ** 2 + b2 ** 2
        ll = l1 * l2
        sqrt_ll = int(ll ** 0.5)
        if sqrt_ll ** 2 != ll:
            raise ValueError

        bis1_a = l2 * a1 - sqrt_ll * a2
        bis1_b = l2 * b1 - sqrt_ll * b2
        bis1_c = l2 * c1 - sqrt_ll * c2

        bis1 = Line(bis1_a, bis1_b, bis1_c, ('bisector1', line1, line2))

        bis2_a = l2 * a1 + sqrt_ll * a2
        bis2_b = l2 * b1 + sqrt_ll * b2
        bis2_c = l2 * c1 + sqrt_ll * c2

        bis2 = Line(bis2_a, bis2_b, bis2_c, ('bisector2', line1, line2))

        result = list({bis1, bis2} - {None})
        result.sort(key=lambda _l: math.atan2(_l.a, -_l.b))

        return result

    @staticmethod
    def get_line_by_point_slope(point: Point, slope: Fraction):
        a = - slope.numerator
        b = slope.denominator
        c = a * point.x + b * point.y
        result = Line(Fraction(a), b, c)
        return result

    def __repr__(self):
        if isinstance(self.obj_tuple, str):
            return self.obj_tuple
        return '<%s * x + %s * y = %s>' % (self.a, self.b, self.c)

    def __hash__(self):
        if self.hash is None:
            self.hash = hash((self.a, self.b, self.c))
        return self.hash

    def __eq__(self, other):
        return (self.a, self.b, self.c) == (other.a, other.b, other.c)

    def __ge__(self, other):
        return (self.a, self.b, self.c) >= (other.a, other.b, other.c)

    def __gt__(self, other):
        return (self.a, self.b, self.c) > (other.a, other.b, other.c)

    def __lt__(self, other):
        return (self.a, self.b, self.c) < (other.a, other.b, other.c)

    def __le__(self, other):
        return (self.a, self.b, self.c) <= (other.a, other.b, other.c)

    def __ne__(self, other):
        return (self.a, self.b, self.c) != (other.a, other.b, other.c)

    def details(self):
        if self.obj_tuple is None:
            return str(self)
        if isinstance(self.obj_tuple, str):
            return self.obj_tuple
        else:
            return "%s(%s,%s)" % (self.obj_tuple[0], self.obj_tuple[1].details(), self.obj_tuple[2].details())


def test_main():
    pb = Point(Fraction(4) - 3, Fraction(1) - 3, "B")
    pc = Point(Fraction(1) - 3, Fraction(2) - 3, "C")
    la = Line.get_line_contains_points(pb, pc)
    p1 = Point(Fraction(5) - 3, Fraction(3) - 3, "p1")
    p2 = Point(Fraction(5) - 3, Fraction(4) - 3, "p2")
    lc = Line.get_line_contains_points(pb, p1)
    lb = Line.get_line_contains_points(pc, p2)
    pa = Line.get_cross_point(lb, lc)
    px = Point(pa.x + 1, pa.y + 1, "px")
    lt = Line.get_line_contains_points(pa, px)
    pm = la.get_cross_point(lt)
    Lc = Line.get_line_parallel_to(lc, pm)
    Lb = Line.get_line_parallel_to(lb, pm)
    PC = Line.get_cross_point(Lc, lb)
    PB = Line.get_cross_point(Lb, lc)
    L = Line.get_line_contains_points(PB, PC)
    print(L)
    print((pa.l2(PB), pa.l2(PC)))
    print((pm.l2(PB), pm.l2(PC)))
    print(lb.contain_point(PC))
    print(lc.contain_point(PB))
    print(la.contain_point(pm))

    print(pa.middle(pm))

    ll = Line.get_bisectors_for_2lines(lb, lc)
    print(ll)


if __name__ == "__main__":
    test_main()
