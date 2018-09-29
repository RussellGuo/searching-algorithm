import itertools
import time
from fractions import Fraction

from draw_searching_graph import draw_result
from figure import Figure
from geo import Point, Line


def figure_symmetry_all(lines):
    def figure_symmetry_hv(_lines):
        figs = {tuple(sorted([(line[0], +line[1], +line[2]) for line in _lines])),
                tuple(sorted([(line[0], -line[1], +line[2]) for line in _lines])),
                tuple(sorted([(line[0], +line[1], -line[2]) for line in _lines])),
                tuple(sorted([(line[0], -line[1], -line[2]) for line in _lines]))}
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
    return figs1 | figs2


def test_sym():
    a = ((5, 1, 8), (5, 19, -10), (43, 76, -109))
    b = figure_symmetry_all(a)
    print(a, b)
    for f in b:
        fig = Figure.build_figure_by_params_of_lines(f, True)
        draw_result(fig, Point(0, 0))


def get_points_in_two_lines_set(lines_a, lines_b):
    points = set(a.get_cross_point(b) for a, b in itertools.product(lines_a, lines_b)) - {None}
    return points


def get_points_in_one_lines_set(lines):
    points = set(a.get_cross_point(b) for a, b in itertools.combinations(lines, 2)) - {None}
    return points


def all_lines_for_points(points):
    lines = set(Line.get_line_contains_points(a, b) for a, b in itertools.combinations(points, 2))
    return lines


def get_fig_level(fig):
    return len(fig)


def bfs_dump_for_pythagorea(init_param_lines, coord_grid=3, max_depth=3):
    line_tab = {}
    fig_tab = set()
    point_tab = {}

    def pointer_checker(x: Fraction, y: Fraction) -> bool:
        def scale_checker(scale: Fraction) -> bool:
            return abs(scale.numerator) <= abs(scale.denominator) * coord_grid

        return scale_checker(x) and scale_checker(y)

    def get_ref_of_line(abc):
        try:
            ref = line_tab[abc]
        except KeyError:
            ref = line_tab[abc] = abc
        return ref

    def list_of_fig_which_has_point(point):
        point_vector = (point.x.numerator, point.x.denominator, point.y.numerator, point.y.denominator)
        try:
            fig_list = point_tab[point_vector]
        except KeyError:
            fig_list = point_tab[point_vector] = []
            if len(point_tab) % 10000 == 0:
                print(len(point_tab), time.time())

        return fig_list

    init_lines = set([Line(i[0], i[1], i[2]) for i in init_param_lines])
    init_points = get_points_in_one_lines_set(init_lines)

    init_fig = ()
    fig_tab.add(init_fig)
    for p in init_points:
        fig_lst = list_of_fig_which_has_point(p)
        fig_lst.append(init_fig)

    # create first_level_lines, it's for speed up to generate every new potential lines for next level
    # for all_lines = init_lines + current_lines,
    #    next lines will be all_point * all_point - init_lines - current_lines
    # and all_point = init_point + new_points; then
    #   all_point * all_point = init_point * init_point + init_points * new_point + new_point * new_point
    #   new_point * new_point must be the old line, init_point * init_point is pre-calculated.
    #   so we just care init_points * new_point and pre-calculated lines.
    first_level_lines = all_lines_for_points(init_points) - init_lines
    for line in first_level_lines:
        get_ref_of_line((line.a, line.b, line.c))

    for level in range(max_depth + 1):
        print(level, time.time())
        current_figure_set = [fig for fig in fig_tab if get_fig_level(fig) == level]
        print(level, len(current_figure_set), time.time())
        for cur_fig in current_figure_set:
            # find all the point and record them
            # should use all lines cross (all lines + init_lines)
            geo_lines = set([Line(i[0], i[1], i[2]) for i in cur_fig])
            all_lines = geo_lines | init_lines
            it = itertools.product(geo_lines, all_lines)
            new_points = set()
            for line_a, line_b in it:
                p = line_a.get_cross_point(line_b, pointer_checker)
                if p and p not in new_points:
                    new_points.add(p)

                    # added into point->figure table if it's worth
                    p_fig_list = list_of_fig_which_has_point(p)
                    p_exists_in_lower = p_fig_list and get_fig_level(p_fig_list[0]) < level
                    if not p_exists_in_lower:
                        p_fig_list.append(cur_fig)

            # produce next level
            if level == max_depth:
                continue  # no need to do for the last level
            new_lines = set([Line.get_line_contains_points(p0, p1) for p0, p1 in
                             itertools.product(new_points, new_points | init_points)]) - {None}
            for line in new_lines | first_level_lines:
                if line and line not in all_lines:  # is different with current
                    line_param = get_ref_of_line((line.a, line.b, line.c))
                    new_fig = tuple(sorted(cur_fig + (line_param,)))
                    new_figs = figure_symmetry_all(new_fig)
                    for fig in new_figs:
                        if fig in fig_tab:
                            break
                    else:
                        fig_tab.add(new_fig)

    print(len(point_tab), len(fig_tab), len(line_tab), time.time())
    print(point_tab.__sizeof__(), fig_tab.__sizeof__(), line_tab.__sizeof__(), time.time())

    return point_tab


def get_pythagorea_graph():
    coord_grid = 3
    init_param_lines = []
    for i in range(-coord_grid, coord_grid + 1):
        init_param_lines.append((0, 1, i), )
        init_param_lines.append((1, 0, i), )
    init_param_lines.sort()
    point_tab = bfs_dump_for_pythagorea(init_param_lines, coord_grid, 3)
    return point_tab


def test_bfs_dump():
    point_tab = get_pythagorea_graph()
    pass  # set breakpoint here for debugging


if __name__ == '__main__':
    # test_sym()
    test_bfs_dump()
