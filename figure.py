from geo import Point, Line
import fractions


class Figure: pass


class Figure:
    def __init__(self, points, lines):
        self.points = tuple(points)
        self.lines = tuple(lines)

    def __eq__(self, other: Figure):
        return  self.points == other.points and self.lines == other.lines

    def __hash__(self):
        return hash((self.points, self.lines))

if __name__ == "__main__":
    f1 = Figure([Point(fractions.Fraction(2, 3), fractions.Fraction(1, 1))], [])
    f2 = Figure([Point(fractions.Fraction(4, 6), fractions.Fraction(1, 1))], [])
    f=set([f1,f2])
    print(f)