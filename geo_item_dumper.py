from fractions import Fraction
from typing import FrozenSet

from figure import Figure
from geo import Point, Line


class GeoItemDumperBase:
    def __init__(self):
        pass

    def new_root(self, fig_root: Figure):
        pass

    def new_figure(self, f: Figure, l: Line, new_points: FrozenSet[Point]):
        pass


class GeoItemDumperConsole:
    def __init__(self):
        super(GeoItemDumperConsole, self).__init__()
        self.figure_count = self.line_count = self.point_count = 0

    def new_root(self, fig: Figure):
        self.figure_count += 1
        self.line_count += len(fig.lines)
        self.point_count += len(fig.new_points) + len(fig.base_points)
        pass

    def new_figure(self, f: Figure, l: Line, new_points: FrozenSet[Point]):
        self.figure_count += 1
        self.line_count += 1
        self.point_count += len(new_points)
        pass

    def close(self):
        print(self.point_count, self.line_count, self.figure_count)
        pass


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
    result = search(exam_figure, point_target, 2, dumper)
    dumper.close()

    return result


if __name__ == "__main__":
    fig, point = dump_every_graph()
    print(Point.id, Line.id, Figure.id)
