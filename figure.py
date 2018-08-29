import fractions

from geo import Point, Line


class Figure:
    def __init__(self, parent, line, new_point_checker=None):

        self.new_point_checker = new_point_checker or parent.new_point_checker
        base_lines = parent.lines if parent else frozenset()
        self.lines = frozenset(base_lines | {line})
        self.hash = hash(self.lines)

        self.base_points = frozenset(parent.base_points | parent.new_points) if parent else frozenset()
        new_points = set()
        for l in self.lines:
            p = line.get_cross_point(l, self.new_point_checker)
            if p and p not in self.base_points:
                new_points.add(p)
        self.new_points = frozenset(new_points)

    def get_new_potential_lines(self, for_new_point_only=False):
        lines = set()

        def append_line(p1, p2):
            l = Line.get_line_contains_points(p1, p2)
            if l and l not in self.lines:
                lines.add(l)

        if for_new_point_only:
            for p_1 in self.new_points:
                for p_2 in self.base_points:
                    append_line(p_1, p_2)
        else:
            points = tuple(sorted(self.new_points | self.base_points))
            for i in range(len(points)):
                p_1 = points[i]
                for j in range(i + 1, len(points)):
                    p_2 = points[j]
                    append_line(p_1, p_2)
        return lines

    def is_different_from_parent(self):
        return len(self.new_points) > 0

    def __eq__(self, other):
        return self.lines == other.lines

    def __hash__(self):
        return self.hash

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
    for p in init_figure.new_points | init_figure.base_points:
        p.obj_list = "P%d%d" % (p.y, p.x)

    return init_figure


def search(figure: Figure, point_target: Point):
    current_figure_set = {figure}

    try:
        for i in range(10):
            print(i, len(current_figure_set))
            next_figure_set = set()
            while len(current_figure_set) > 0:
                fig = current_figure_set.pop()
                lines = (fig.get_new_potential_lines(i > 0))
                for l in lines:
                    f = Figure(fig, l)
                    if f.is_different_from_parent and f not in next_figure_set:
                        if point_target in f.new_points:
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
            print(l)
        for p in o.new_points:
            if p == point_target:
                print(p.details())
                break


def exam_22_17():
    init_figure = get_init_figure()

    # create the example figure
    exam_figure = init_figure

    line_a = Line(fractions.Fraction(1), fractions.Fraction(+3), fractions.Fraction(17), "a")
    line_b = Line(fractions.Fraction(1), fractions.Fraction(-2), fractions.Fraction(-3), "b")
    line_c = Line(fractions.Fraction(2), fractions.Fraction(-1), fractions.Fraction(-1), "c")

    line_m = Line(fractions.Fraction(5), fractions.Fraction(3), fractions.Fraction(30), "m")

    line_t1 = Line(fractions.Fraction(19), fractions.Fraction(33), fractions.Fraction(213), "t1")
    line_t2 = Line(fractions.Fraction(19), fractions.Fraction(-2), fractions.Fraction(38), "t2")

    line_t3 = Line(fractions.Fraction(24), fractions.Fraction(-12), fractions.Fraction(23), "t3")
    line_t4 = Line(fractions.Fraction(12), fractions.Fraction(-24), fractions.Fraction(-71), "t4")

    exam_figure = Figure(exam_figure, line_a)
    exam_figure = Figure(exam_figure, line_b)
    exam_figure = Figure(exam_figure, line_c)

    exam_figure = Figure(exam_figure, line_m)
    exam_figure = Figure(exam_figure, line_t1)
    exam_figure = Figure(exam_figure, line_t2)
    exam_figure = Figure(exam_figure, line_t3)
    # exam_figure = Figure(exam_figure, line_t4)

    # this is the root
    exam_figure.parent = None

    # try to find it
    point_target = Point(fractions.Fraction(47, 36), fractions.Fraction(65, 18), "Target")
    # point_target = Point(fractions.Fraction(43, 24), fractions.Fraction(25, 8), "Target")
    search(exam_figure, point_target)

    # <>(P06,X(<>(P23,X(c,H4)),b)) for <47/36, 65/18>
    # <>(X(<>(P05,X(a,V4)),H2),P31) for <41/18, 95/36>
    # <>(P06,P53) for <13/4, 55/12>
    # <>(P02,X(<>(P36,X(lm,a)),H5)) for <41/18, 95/36>, too
    # X( <> (X(b, V2), X(c, H4)), <> (P42, X(m, c))) for <43/24, 25/8>


def exam_27_14():
    init_figure = get_init_figure()

    # create the example figure
    exam_figure = init_figure
    line_1 = Line(fractions.Fraction(1), fractions.Fraction(1), fractions.Fraction(6), "line6")
    exam_figure = Figure(exam_figure, line_1)
    # this is the root
    exam_figure.parent = None

    # try to find it
    point_target = Point(fractions.Fraction(35, 12), fractions.Fraction(37, 12), "Target")
    search(exam_figure, point_target)


if __name__ == "__main__":
    exam_27_14()
