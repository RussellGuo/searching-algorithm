import pickle
import sys


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
    from fractions import Fraction

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
        print("the BFS searching result NOT ready, building it", file=sys.stderr)
        data = bfs_for_pythagorea.get_pythagorea_graph()

        # save if
        print("Saving BFS searching result into a pickle file", file=sys.stderr)
        with open(cache_file_name, "wb") as write_f:
            pickle.dump(data, write_f, -1)
        del data

        # try again
        ret = get_cached_data()

    assert ret
    return ret


def normalized_line(line):
    a, b, c = line
    if a < 0 or a == 0 and b < 0:
        return -a, -b, -c
    else:
        return a, b, c


def get_symmetry_matrix_table():
    ret = (
        ((+1, +0), (+0, +1)),
        ((-1, +0), (+0, +1)),
        ((+1, +0), (+0, -1)),
        ((-1, +0), (+0, -1)),
        ((+0, +1), (+1, +0)),
        ((+0, -1), (+1, +0)),
        ((+0, +1), (-1, +0)),
        ((+0, -1), (-1, +0)),
    )
    return ret


def mat_mul(mat, vector):
    r = (mat[0][0] * vector[0] + mat[0][1] * vector[1], mat[1][0] * vector[0] + mat[1][1] * vector[1])
    return r


def apply_mat_on_point(point, mat):
    p0 = mat_mul(mat, (point[0], point[2]))
    pd = mat_mul(mat, (point[1], point[3]))
    p = (p0[0], abs(pd[0]), p0[1], abs(pd[1]))
    return p


def apply_mat_on_figure(figure, mat):
    fig0 = [normalized_line(mat_mul(mat, l[:2]) + (l[2],)) for l in figure]
    return fig0


def iter_of_figure_and_point_symmetry(point, fig_list):
    for mat in get_symmetry_matrix_table():
        p = apply_mat_on_point(point, mat)
        for fig in fig_list:
            fig0 = apply_mat_on_figure(fig, mat)
            yield (p, tuple(fig0))


def inv_for_symmetry_mat(mat):
    det = mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
    assert abs(det) == 1
    inv_mat = ((mat[1][1] // det, -mat[0][1] // det), (-mat[1][0] // det, mat[0][0] // det))
    return inv_mat
