import sqlite3
from fractions import Fraction

from draw_searching_graph import draw_result
from figure import Figure
from geo import Point


class NewDBQuery:
    from create_new_db_from_bin import NewDBCreator
    db_file_name = NewDBCreator.db_file_name

    def __init__(self):
        self.db_file_name = NewDBQuery.db_file_name
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
            fig = Figure.build_figure_by_params_of_lines(lines, True)
            p = fig.find_point(point)
            result.append((p, fig))
            cursor.close()

        return result


def main():
    db_query = NewDBQuery()
    p = Point(Fraction(5339, 1794), Fraction(919, 299))
    p = Point(Fraction(1, 3), Fraction(3, 1))
    r = db_query.query_point(p)
    for re in r:
        p, f = re
        draw_result(f, p)
    pass


if __name__ == '__main__':
    main()
