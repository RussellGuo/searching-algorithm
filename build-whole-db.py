import array

from draw_searching_graph import draw_result
from figure import get_init_figure, Figure
from geo import Point, Line


class GraphMemoryDumper:
    def __init__(self, init_figure: Figure = None):
        self.last_id_of_figure = self.last_id_of_line = self.last_id_of_point = 0
        self.line_memory_table = {}
        self.point_memory_table = {}
        self.figure_memory_table = {}
        if init_figure is None:
            init_figure = get_init_figure()
        self.init_lines = init_figure.lines
        self.point_checker = init_figure.new_point_checker

    def append_figure_by_params_of_lines(self, figure_params):
        lines = tuple(sorted(figure_params))
        level = len(lines)
        self.last_id_of_figure += 1
        id_of_figure = self.last_id_of_figure

        line_id_list = [self.get_line_id_by_param(line_param) for line_param in figure_params]
        line_id_list.sort()
        self.figure_memory_table[tuple(line_id_list)] = (id_of_figure, level)

        lines_object = [Line(line[0], line[1], line[2]) for line in lines]
        for init_line in self.init_lines:
            for line in lines_object:
                p = line.get_cross_point(init_line, self.point_checker)
                self.save_into_point_table_etc(id_of_figure, level, p)
        for i in range(len(lines_object)):
            for j in range(i + 1, len(lines_object)):
                p = lines_object[i].get_cross_point(lines_object[j], self.point_checker)
                self.save_into_point_table_etc(id_of_figure, level, p)

    def get_line_id_by_param(self, abc):
        if abc in self.line_memory_table:
            return self.line_memory_table[abc]

        self.last_id_of_line += 1
        id_of_line = self.last_id_of_line
        self.line_memory_table[abc] = id_of_line
        return id_of_line

    def save_into_point_table_etc(self, fig_id: int, fig_level: int, point: Point):
        if point is None:
            return
        point_vector = (point.x.numerator, point.x.denominator, point.y.numerator, point.y.denominator)

        # find point_id
        if point_vector in self.point_memory_table:
            point_id, level = self.point_memory_table[point_vector]
            if level < fig_level:
                return  # no need to save this point into point_figure table
        else:
            self.last_id_of_point += 1
            point_id = self.last_id_of_point
            self.point_memory_table[point_vector] = (point_id, fig_level)


def figure_symmetry_all(lines):
    def figure_symmetry_hv(_lines):
        figs = [tuple(sorted([(line[0], +line[1], +line[2]) for line in _lines])),
                tuple(sorted([(line[0], -line[1], +line[2]) for line in _lines])),
                tuple(sorted([(line[0], +line[1], -line[2]) for line in _lines])),
                tuple(sorted([(line[0], -line[1], -line[2]) for line in _lines]))]
        return figs

    def figure_swap_xy(_lines):
        new_lines = []
        for line in _lines:
            a, b, c = line
            if b < 0:
                a, b, c = -a, -b, -c
            new_lines.append((b, a, c))
        return new_lines

    figs1 = figure_symmetry_hv(lines)
    figs2 = figure_symmetry_hv(figure_swap_xy(lines))
    return sorted(set(figs1 + figs2))


def get_line_normalized(line):
    n_line = list(line[:])
    vector = [False, False, False, False]
    for i in range(3):
        if n_line[i] < 0:
            n_line[i] = - n_line[i]
            vector[i] = True
    if n_line[0] > n_line[1]:
        n_line[0], n_line[1] = n_line[1], n_line[0]
        vector[3] = True
    return n_line[0:3], vector


def bin_figure_iter():
    max_depth = 3
    for dep in range(max_depth):
        no = dep + 1
        with open("figure-level%d.bin" % no, "rb") as f:
            while True:
                bin_record = array.array("h")
                try:
                    bin_record.fromfile(f, no * 3)
                except EOFError:
                    break
                a = bin_record.tolist()
                vv = []
                for i in range(no):
                    v = a[i * 3:(i + 1) * 3]
                    v[2] -= 3 * (v[0] + v[1])
                    vv.append(tuple(v))
                vv.sort()
                all = figure_symmetry_all(vv)
                if all[0] == tuple(vv):
                    yield vv


def main():
    dumper = GraphMemoryDumper()
    i = 0
    for f in bin_figure_iter():
        i += 1
        if i % 10000 == 0:
            print(i)
        pass
    print(i)


def test():
    a = ((1, 1, 0), (2, 1, 0))
    b = figure_symmetry_all(a)
    print(a, b)
    for f in b:
        fig = Figure.build_figure_by_params_of_lines(f, True)
        draw_result(fig, Point(0, 0))

    pass


if __name__ == '__main__':
    main()
