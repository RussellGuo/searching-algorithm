import fractions
import math


class Line: pass


class Point:
    def __init__(self, x: fractions.Fraction, y: fractions.Fraction, obj_list=None):
        self.x = x
        self.y = y
        self.obj_list = obj_list

    def __repr__(self):
        if isinstance(self.obj_list, str):
            return self.obj_list
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

    def details(self):
        if self.obj_list is None:
            return str(self)
        if isinstance(self.obj_list, str):
            return self.obj_list
        else:
            return "%s(%s,%s)" % (self.obj_list[0], self.obj_list[1].details(), self.obj_list[2].details())

    def middle(self, other):
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2, ["-", self, other])

    def l2(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2


class Line:
    def __init__(self, _a: fractions.Fraction, _b: fractions.Fraction, _c: fractions.Fraction, obj_list=None):
        self.a = fractions.Fraction(_a)
        self.b = fractions.Fraction(_b)
        self.c = fractions.Fraction(_c)
        self.obj_list = obj_list

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
            self.__shadow_c *= -1

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
        return Point(x, y, ["X", self, other])

    @staticmethod
    def get_line_contains_points(p1: Point, p2: Point) -> Line:
        if p1 == p2:
            return None
        a = p1.y - p2.y
        b = p2.x - p1.x
        c = p2.x * p1.y - p1.x * p2.y
        line = Line(a, b, c, ["<>", p1, p2])
        return line

    @staticmethod
    def get_line_parallel_to(other: Line, p: Point) -> Line:
        if other is None or p is None:
            return None
        a = other.__shadow_a
        b = other.__shadow_b
        c = a * p.x + b * p.y
        line = Line(a, b, c, ["//", other, p])
        return line

    @staticmethod
    def get_line_perpendicular_to(other: Line, p: Point) -> Line:
        if other is None or p is None:
            return None
        a = other.__shadow_b
        b = -other.__shadow_a
        c = a * p.x + b * p.y
        line = Line(a, b, c, ["-|", other, p])
        return line

    def __repr__(self):
        if isinstance(self.obj_list, str):
            return self.obj_list
        return '<%s * x + %s * y = %s>' % (self.__shadow_a, self.__shadow_b, self.__shadow_c)

    def __hash__(self):
        return hash((self.__shadow_a, self.__shadow_b, self.__shadow_c))

    def __eq__(self, other: Line):
        return self.__shadow_a == other.__shadow_a and self.__shadow_b == other.__shadow_b and self.__shadow_c == other.__shadow_c

    def details(self):
        if self.obj_list is None:
            return str(self)
        if isinstance(self.obj_list, str):
            return self.obj_list
        else:
            return "%s(%s,%s)" % (self.obj_list[0], self.obj_list[1].details(), self.obj_list[2].details())


if __name__ == "__main__":
    pb = Point(fractions.Fraction(2), fractions.Fraction(5), "B")
    pc = Point(fractions.Fraction(5), fractions.Fraction(4), "C")
    la = Line.get_line_contains_points(pb, pc)
    p1 = Point(fractions.Fraction(1), fractions.Fraction(3), "p1")
    p2 = Point(fractions.Fraction(1), fractions.Fraction(2), "p2")
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
    pass
