import copy
import sqlite3
from fractions import Fraction

from draw_searching_graph import draw_result
from figure import Figure, get_standard_pointer_checker
from geo import Point, Line


class Searching:
    db_file_name = 'graph.db'

    def __init__(self):
        self.connect = sqlite3.connect(Searching.db_file_name)
        cursor = self.connect.cursor()

        self.prepare_database()

        # to find all the init-figure, points and lines

        # init figure
        cursor.execute('select * from init_figure')
        init_figure_row = cursor.fetchall()
        cursor.close()
        assert (len(init_figure_row) == 1)
        self.init_figure_id = init_figure_row[0][0]

        # init lines
        self.init_lines = {}
        cursor = self.connect.cursor()
        cursor.execute('select * from init_line')
        for line in cursor:
            line_id, line_a, line_b, line_c, p1_id, p2_id = line
            assert (p1_id, p2_id) == (0, 0)
            # build a name for this line
            if line_a == 0 and line_b == 1:
                name = 'H%d' % line_c
            elif line_a == 1 and line_b == 0:
                name = 'V%d' % line_c
            else:
                name = '<%dx+%dy=%d>' % (line_a, line_b, line_c)
            line = Line(line_a, line_b, line_c, name)
            self.init_lines[line_id] = line
        cursor.close()

        # init_figure created
        self.init_figure = None
        for line in self.init_lines.values():
            self.init_figure = Figure(self.init_figure, line, get_standard_pointer_checker())
        self.init_figure.parent = None

        # init points
        self.init_points = {}
        cursor = self.connect.cursor()
        cursor.execute('select * from init_point')
        points_in_db = cursor.fetchall()
        cursor.close()
        assert len(points_in_db) == len(self.init_figure.base_points) + len(self.init_figure.new_points)
        for point_db in points_in_db:
            point_id, x_numerator, x_denominator, y_numerator, y_denominator, line1_id, line2_id = point_db
            assert (line1_id, line2_id) == (0, 0)
            point = Point(Fraction(x_numerator, x_denominator), Fraction(y_numerator, y_denominator))
            p = self.init_figure.find_point(point)
            self.init_points[point_id] = p
            if x_denominator == y_denominator == 1:
                p.obj_tuple = "P%d%d" % (y_numerator, x_numerator)
            else:
                p.obj_tuple = "P(%d/%d,%d/%d)" % (y_numerator, y_denominator, x_numerator, x_denominator)

    def prepare_database(self):
        cmds = (
            "create table if not exists init_line as select * from line where point1_id = 0 or point2_id = 0",
            "create table if not exists init_point  as select * from point where line1_id = 0 or line2_id = 0",
            "create table if not exists init_figure as select * from figure where parent_id = 0",
            "create unique index if not exists figure_id_idx on figure(id)",
            "create unique index if not exists point_id_idx on point(id)",
            "create unique index if not exists line_id_idx on line(id)",
            "create index if not exists point_value_idx on point" 
            "(x_numerator, x_denominator, y_numerator, y_denominator)",
            "create unique index if not exists line_id_to_figure_id_idx on figure(line_id)"
        )
        cursor = self.connect.cursor()
        for cmd in cmds:
            cursor.execute(cmd)
        cursor.close()

    def search_point_id_list(self, point: Point):
        sql_smt = 'select id from point where x_numerator = ? and x_denominator = ? and ' + \
                  'y_numerator = ? and y_denominator = ? order by id'
        cond = (point.x.numerator, point.x.denominator, point.y.numerator, point.y.denominator)
        cursor_searching_points = self.connect.cursor()
        cursor_searching_points.execute(sql_smt, cond)
        search_result = []
        depth = 0
        for point_id in cursor_searching_points:
            fig_id = self.get_figure_id_from_point_id(point_id[0])
            fig = self.build_figure_by_id(fig_id)

            dep = fig.level()
            if depth == 0:
                depth = dep
            if dep > depth:
                break
            point_found = fig.find_point(point)
            search_result.append((point_found, fig))

        cursor_searching_points.close()
        return search_result

    def build_figure_by_id(self, fig_id) -> Figure:
        if fig_id == self.init_figure_id:
            return copy.deepcopy(self.init_figure)

        # recursive building
        # 1st, find the parent
        cursor = self.connect.cursor()
        cursor.execute('select parent_id, line_id from figure where id = ?', (fig_id,))
        row = cursor.fetchall()
        cursor.close()
        assert len(row) == 1
        parent_id, line_id = row[0]
        parent = self.build_figure_by_id(parent_id)

        # 2nd, find the line
        cursor = self.connect.cursor()
        cursor.execute("select point1_id, point2_id from line where id = ?", (line_id,))
        row = cursor.fetchall()
        cursor.close()
        assert len(row) == 1

        points = []
        for point_id in row[0]:
            cursor = self.connect.cursor()
            sql_smt = "select x_numerator, x_denominator, y_numerator, y_denominator from point where id = ?"
            cursor.execute(sql_smt, (point_id,))
            row = cursor.fetchall()
            cursor.close()
            assert len(row) == 1
            x_numerator, x_denominator, y_numerator, y_denominator = row[0]
            point = Point(Fraction(x_numerator, x_denominator), Fraction(y_numerator, y_denominator), "temp")
            p = parent.find_point(point)
            points.append(p)
        line = Line.get_line_contains_points(points[0], points[1])

        # 3rd, finished it
        fig = Figure(parent, line)
        return fig

    def get_figure_id_from_point_id(self, point_id: int) -> int:

        if point_id in self.init_points:
            return self.init_figure_id

        sql_smt = 'select line1_id, line2_id from point where id = ?'
        cursor = self.connect.cursor()
        cursor.execute(sql_smt, (point_id,))
        row = cursor.fetchall()
        cursor.close()
        assert len(row) == 1
        line_id = max(row[0])

        cursor = self.connect.cursor()
        cursor.execute('select id from figure where line_id = ?', (line_id,))
        row = cursor.fetchall()
        cursor.close()
        assert len(row) == 1

        return row[0][0]


def test():
    s = Searching()
    r = s.search_point_id_list(Point(Fraction(1, 1), Fraction(1, 2)))
    for re in r:
        f, p = re
        draw_result(p, f)
    pass


if __name__ == '__main__':
    test()
