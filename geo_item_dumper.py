from fractions import Fraction
from typing import FrozenSet, Tuple

from figure import Figure
from geo import Point, Line


class GeoItemDumperBase:
    def __init__(self):
        self.figure_count = self.line_count = self.point_count = 0
        pass

    def open(self):
        pass

    def close(self):
        pass

    def output_figure(self, values: Tuple[int, int, int]):
        pass

    def output_line(self, values: Tuple[int, int, int, int, int, int]):
        pass

    def output_point(self, values: Tuple[int, int, int, int, int, int, int]):
        pass

    def new_root(self, fig_root: Figure):
        self.figure_count += 1
        self.line_count += len(fig_root.lines)
        self.point_count += len(fig_root.new_points) + len(fig_root.base_points)
        self.output_figure((fig_root.id, 0, 0))
        for line in fig_root.lines:
            self.output_line((line.id, line.a, line.b, line.c, 0, 0))
        for p in fig_root.new_points | fig_root.base_points:
            self.output_point((p.id, p.x.numerator, p.x.denominator, p.y.numerator, p.y.denominator, 0, 0))

    def new_figure(self, f: Figure, line: Line, new_points: FrozenSet[Point]):
        self.figure_count += 1
        self.line_count += 1
        self.point_count += len(new_points)
        self.output_figure((f.id, f.parent.id, line.id))
        self.output_line((line.id, line.a, line.b, line.c, line.obj_tuple[1].id, line.obj_tuple[2].id))
        for p in new_points:
            self.output_point((p.id, p.x.numerator, p.x.denominator, p.y.numerator, p.y.denominator, p.obj_tuple[1].id,
                               p.obj_tuple[2].id))


class GeoItemDumperConsole(GeoItemDumperBase):

    def output_figure(self, values: Tuple[int, int, int]):
        print(values)

    def output_line(self, values: Tuple[int, int, int, int, int, int]):
        print(values)

    def output_point(self, values: Tuple[int, int, int, int, int, int, int]):
        print(values)

    def close(self):
        print(self.point_count, self.line_count, self.figure_count)


def dump_every_graph():
    from figure import get_init_figure, search
    init_figure = get_init_figure()

    # create the example figure
    exam_figure = init_figure
    # this is the root
    exam_figure.parent = None

    # try to find it
    point_target = Point(Fraction(-1), Fraction(0), "UNTOUCHABLE")
    dumper = GeoItemDumperConsole()
    dumper.open()
    search(exam_figure, point_target, 3, dumper)
    dumper.close()


if __name__ == "__main__":
    dump_every_graph()
    print(Point.id, Line.id, Figure.id)
