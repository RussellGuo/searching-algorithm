import pickle


class Graph:
    __line_cache = {}
    __figure_cache = {}

    def __init__(self, output_name):
        self.output_file = output_name
        self.point_figure_table = {}

    @staticmethod
    def get_ref_from_cache(a_dict, value):
        try:
            ref = a_dict[value]
        except KeyError:
            ref = a_dict[value] = value

        return ref

    def add_point_figure_relation(self, point, figure):
        sorted_figure = tuple(sorted(figure))

        # lines processing
        lines = []
        for line in sorted_figure:
            ll = Graph.get_ref_from_cache(Graph.__line_cache, line)
            lines.append(ll)
        lines.sort()

        # figure processing
        fig = tuple(lines)
        ref_fig = Graph.get_ref_from_cache(Graph.__figure_cache, fig)

        # point -> figure processing
        if point not in self.point_figure_table:
            self.point_figure_table[point] = []
        fig_list_for_point = self.point_figure_table[point]
        if ref_fig not in fig_list_for_point:
            if len(fig_list_for_point) > 0:
                fig_level_in_list = len(fig_list_for_point[0])
                cur_level = len(ref_fig)
                if cur_level > fig_level_in_list:
                    return
                elif cur_level < fig_level_in_list:
                    fig_list_for_point.clear()
            fig_list_for_point.append(ref_fig)

        pass

    def close(self):
        with open(self.output_file, "w") as f:
            #
            while self.point_figure_table:
                point, fig_list = self.point_figure_table.popitem()
                for fig in fig_list:
                    f.write(str((point, fig)) + "\n")
            pass


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


def test():
    total_data = pickle.load(open("points.185", "rb"))
    total_graph = Graph("points.185.txt")
    while total_data:
        point, fig_list = total_data.popitem()
        ll = len(total_data)
        if ll % 10000 == 0:
            print(ll)
        for fig in fig_list:
            total_graph.add_point_figure_relation(point, fig)
    del total_data
    total_graph.close()
    del total_graph

    for file_name in ("point_to_figure.pickle",):
        with open(file_name, 'rb') as f:
            io_data = pickle.load(f)
            whole_data = Graph(file_name + ".txt")
            while io_data:
                point, fig_list = io_data.popitem()
                ll = len(io_data)
                if ll % 10000 == 0:
                    print(ll)
                for p_f_pair in iter_of_figure_and_point_symmetry(point, fig_list):
                    new_point, new_fig = p_f_pair
                    whole_data.add_point_figure_relation(new_point, new_fig)
            del io_data
            whole_data.close()
            del whole_data


if __name__ == '__main__':
    test()
