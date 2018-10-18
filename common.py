import pickle
from fractions import Fraction


def GRID_SIZE():
    return 3


def INIT_FIGURE():
    coord_grid = GRID_SIZE()
    init_lines = []
    for i in range(-coord_grid, coord_grid + 1):
        init_lines.append((0, 1, i), )
        init_lines.append((1, 0, i), )
    init_lines.sort()
    return init_lines


def POINT_CHECKER(grid_size):
    def point_checker(x: Fraction, y: Fraction) -> bool:
        def scale_checker(scale: Fraction) -> bool:
            return abs(scale.numerator) <= abs(scale.denominator) * grid_size

        return scale_checker(x) and scale_checker(y)
    return point_checker


def get_cached_pythagorea_graph(cache_file_name="point_to_figure.pickle"):
    import bfs_for_pythagorea

    def get_cached_data():
        try:
            with open(cache_file_name, "rb") as read_f:
                result = pickle.load(read_f)
            return result
        except FileNotFoundError:
            return None

    ret = get_cached_data()
    if not ret:
        # generated it
        data = bfs_for_pythagorea.get_pythagorea_graph()

        # save if
        with open(cache_file_name, "wb") as write_f:
            pickle.dump(data, write_f, -1)
        del data

        # try again
        ret = get_cached_data()

    assert ret
    return ret


def iter_of_figure_and_point_symmetry(point, fig_list):
    def mat_mul(mat, vector):
        r = (mat[0][0] * vector[0] + mat[0][1] * vector[1], mat[1][0] * vector[0] + mat[1][1] * vector[1])
        return r

    def normalized_line(line):
        a, b, c = line
        if a < 0 or a == 0 and b < 0:
            return -a, -b, -c
        else:
            return a, b, c

    for _mat in (
            ((+1, +0), (+0, +1)),
            ((-1, +0), (+0, +1)),
            ((+1, +0), (+0, -1)),
            ((-1, +0), (+0, -1)),
            ((+0, +1), (+1, +0)),
            ((+0, -1), (+1, +0)),
            ((+0, +1), (-1, +0)),
            ((+0, -1), (-1, +0)),
    ):
        p0 = mat_mul(_mat, (point[0], point[2]))
        pd = mat_mul(_mat, (point[1], point[3]))
        p = (p0[0], abs(pd[0]), p0[1], abs(pd[1]))
        for fig in fig_list:
            fig0 = [normalized_line(mat_mul(_mat, l[:2]) + (l[2],)) for l in fig]
            yield (p, tuple(fig0))
