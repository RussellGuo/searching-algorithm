import fractions

from geo import Point, Line


class Figure: pass


class Figure:
    def __init__(self, parent: Figure, line: Line, new_point_checker=None, target_point=None):
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
        self.found = target_point is not None and target_point in self.points

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


def get_init_figure():
    zero = fractions.Fraction(0)
    one = fractions.Fraction(1)
    max_ = fractions.Fraction(6)
    init_figure = None

    def my_new_point_checker(x: fractions.Fraction, y: fractions.Fraction):
        return max_ >= x >= zero and max_ >= y >= zero

    for i in range(7):
        step = fractions.Fraction(i)
        horn_line = Line(zero, one, step, "H%d" % i)
        vert_line = Line(one, zero, step, "V%d" % i)
        init_figure = Figure(init_figure, horn_line, my_new_point_checker)
        init_figure = Figure(init_figure, vert_line, my_new_point_checker)
    init_figure.parent = None
    for p in init_figure.points:
        p.obj_list = "P%d%d" % (p.y, p.x)

    return init_figure


if __name__ == "__main__":

    # as name
    init_figure = get_init_figure()

    # create the example figure
    exam_figure = init_figure

    line_a = Line(fractions.Fraction(1), fractions.Fraction(+3), fractions.Fraction(17), "a")
    line_b = Line(fractions.Fraction(1), fractions.Fraction(-2), fractions.Fraction(-3), "b")
    line_c = Line(fractions.Fraction(2), fractions.Fraction(-1), fractions.Fraction(-1), "c")

    exam_figure = Figure(exam_figure, line_a)
    exam_figure = Figure(exam_figure, line_b)
    exam_figure = Figure(exam_figure, line_c)

    # this is the root
    exam_figure.parent = None

    # try to find it
    line_target = Line(fractions.Fraction(12), fractions.Fraction(12), fractions.Fraction(59), "target")

    point_target = Point(fractions.Fraction(41, 18), fractions.Fraction(95, 36), "Target")
    current_figure_set = {exam_figure}

    try:
        for i in range(10):
            print(i, len(current_figure_set))
            next_figure_set = set()
            for fig in current_figure_set:
                lines = (fig.get_new_potential_lines())
                for l in lines:
                    f = Figure(fig, l)
                    if f.new_point_count > 0 and f not in next_figure_set:
                        if point_target in f.points:
                            raise StopIteration(f)
                        next_figure_set.add(f)
                        ll = len(next_figure_set)
                        if ll % 200 == 0:
                            print(ll)
            current_figure_set = next_figure_set

        pass  # Not found
    except StopIteration as e:
        o = e.value
        for l in o.lines:
            print(l.details())
        pass

# <>(P06,X(<>(P23,X(c,H4)),b)) for <47/36, 65/18>
# <>(X(<>(P05,X(a,V4)),H2),P31) for <41/18, 95, 36>
# <>(P06,P53) for <13/4, 55/12>
