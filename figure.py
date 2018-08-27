from geo import Point, Line
import fractions


class Figure: pass


class Figure:
    def __init__(self, parent: Figure, line: Line, new_point_checker=None):
        self.parent = parent
        self.new_point_checker = new_point_checker or parent.new_point_checker
        parent_points, parent_lines = (parent.points, parent.lines) if parent else ((), ())
        assert (line not in parent_lines)
        self.lines = parent_lines + (line,)
        new_points = []
        for l in self.lines:
            p = line.get_cross_point(l, self.new_point_checker)
            if p and p not in parent_points and p not in new_points:
                new_points.append(p)
        self.points = tuple(sorted(list(parent_points) + new_points))
        self.new_point_count = len(new_points)

    def get_new_potential_lines(self):
        points = tuple(sorted(self.points))
        lines = []
        for i in range(len(points)):
            p1 = points[i]
            for j in range(i + 1, len(points)):
                p2 = points[j]
                l = Line.get_line_contains_points(p1, p2)
                if l and l not in self.lines and l not in lines:
                    lines.append(l)
        return lines

    def is_different_from_parent(self):
        return self.new_point_count >= 1

    def __eq__(self, other: Figure):
        return self.points == other.points and self.lines == other.lines

    def __hash__(self):
        return hash((self.points, self.lines))

    def __repr__(self):
        points = '\n'.join(str(i) for i in sorted(self.points))
        lines = '\n'.join(str(i) for i in self.lines)

        return '@\n' + points + '@\n#\n' + lines + '\n#'


if __name__ == "__main__":
    zero = fractions.Fraction(0)
    one = fractions.Fraction(1)
    max = fractions.Fraction(6)
    init_figure = None


    def my_new_point_checker(x: fractions.Fraction, y: fractions.Fraction):
        return max >= x >= zero and max >= y >= zero


    for i in range(7):
        step = fractions.Fraction(i)
        horn_line = Line(zero, one, step, "H%d" % i)
        vert_line = Line(one, zero, step, "V%d" % i)
        init_figure = Figure(init_figure, horn_line, my_new_point_checker)
        init_figure = Figure(init_figure, vert_line, my_new_point_checker)
    init_figure.parent = None
    for p in init_figure.points:
        p.obj_list = "P%d%d" % (p.y, p.x)
    print(init_figure)
    lines = (init_figure.get_new_potential_lines())
    ff = set()
    for l in lines:
        f = Figure(init_figure, l)
        if f.new_point_count > 0 and f not in ff:
            ff.add(f)
    ff = set()
