import sqlite3
from fractions import Fraction

import common
from draw_searching_graph import draw_result
from geo import Point


class NewDBQuery:
    def __init__(self, db_file_name='new_graph.db'):
        self.db_file_name = db_file_name
        self.connect = sqlite3.connect(self.db_file_name)

    def query_point(self, point: Point):
        cond = (point.x.numerator, point.x.denominator, point.y.numerator, point.y.denominator)
        sql_smt = 'select figure_id from point, point_figure where point.id = point_figure.point_id and' \
                  ' x_numerator = ? and x_denominator = ? and y_numerator = ? and y_denominator = ?'
        cursor = self.connect.cursor()
        cursor.execute(sql_smt, cond)
        matched_fig_id_list = [row[0] for row in cursor]
        cursor.close()

        result = []
        for matched_fig_id in matched_fig_id_list:
            cursor = self.connect.cursor()
            line_query = 'select a,b,c from line, figure_line where figure_id = ? and line_id = line.id'
            cursor.execute(line_query, (matched_fig_id,))
            lines = cursor.fetchall()
            result.append(tuple(lines))
            cursor.close()

        return result

    def query_point_by_symmetry(self, point):
        point_vector = (point.x.numerator, point.x.denominator, point.y.numerator, point.y.denominator)

        mat_table = common.get_symmetry_matrix_table()
        result = []
        for mat in mat_table:
            p = common.apply_mat_on_point(point_vector, mat)
            p0 = Point(Fraction(p[0], p[1]), Fraction(p[2], p[3]))
            fig_list = self.query_point(p0)
            for fig in fig_list:
                fig0 = common.apply_mat_on_figure(fig, mat)
                result.append( tuple(fig0))
        result = list(set(result))
        result.sort()
        return result


def main():
    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    db_query = NewDBQuery()
    # to find init points
    # select * from point_figure, point
    #     where point.id = point_figure.point_id and figure_id = (select id from figure where level = 0)
    p = Point(Fraction(5339, 1794) - 3, Fraction(919, 299) - 3)
    p = Point(Fraction(1, 3), Fraction(3, 1))
    r = db_query.query_point_by_symmetry(p)
    for re in r[:10]:
        draw_result(re, p, init_figure, grid_size)
    pass


if __name__ == '__main__':
    main()
