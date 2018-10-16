import pickle

from common import get_cached_pythagorea_graph, iter_of_figure_and_point_symmetry


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
        io_data = get_cached_pythagorea_graph(file_name)
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

    # should compare point_to_figure.pickle.txt and points.185.txt, the sorted version.
    #     sort -u point_to_figure.pickle.txt -o point_to_figure.pickle.sorted.txt
    #     sort -u points.185.txt -o points.185.sorted.txt
    #     sha1sum *.sorted.txt
    # if everything is OK, the hash value should be same
    # point_to_figure.pickle was generated by bfs_for_pythagorea.py;
    # points.185 was generated by an alter version of bfs_for_pythagorea.py, which doesn't concern symmetry


if __name__ == '__main__':
    test()
