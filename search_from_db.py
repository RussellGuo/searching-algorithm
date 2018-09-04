import sqlite3
from fractions import Fraction

from figure import Figure
from geo import Point, Line


class Searching:
    db_file_name = 'graph.db'

    def __init__(self):
        self.connect = sqlite3.connect(Searching.db_file_name)
        cursor = self.connect.cursor()

        # to find all the init-figure, points and lines

        # init figure
        cursor.execute('select * from figure where parent_id = 0')
        init_figure_row = cursor.fetchall()
        cursor.close()
        assert (len(init_figure_row) == 1)
        self.init_figure_id = init_figure_row[0][0]

        # init lines
        self.init_lines = {}
        cursor = self.connect.cursor()
        cursor.execute('select * from line where point1_id = 0 or point2_id = 0')
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
            self.init_figure = Figure(self.init_figure, line)
        self.init_figure.parent = None

        # init points
        self.init_points = {}
        cursor = self.connect.cursor()
        cursor.execute('select * from point where line1_id = 0 or line2_id = 0')
        points_in_db = cursor.fetchall()
        cursor.close()
        assert len(points_in_db) == len(self.init_figure.base_points) + len(self.init_figure.new_points)
        for point_db in points_in_db:
            point_id, x_numerator, x_denominator, y_numerator, y_denominator, line1_id, line2_id = point_db
            assert (line1_id, line2_id) == (0, 0)
            point = Point(Fraction(x_numerator, x_denominator), Fraction(y_numerator, y_denominator))
            for p in self.init_figure.base_points | self.init_figure.new_points:
                if p == point:
                    self.init_points[point_id] = p
                    if x_denominator == y_denominator == 1:
                        p.obj_tuple = "P%d%d" % (y_numerator, x_numerator)
                    else:
                        p.obj_tuple = "P(%d/%d,%d/%d)" % (y_numerator, y_denominator, x_numerator, x_denominator)
                    break
            else:
                assert False

        pass

    def search_point_id_list(self, point: Point):
        sql_smt = 'select id from point where x_numerator = ? and x_denominator = ? and ' + \
                  'y_numerator = ? and y_denominator = ? order by id'
        cond = (point.x.numerator, point.x.denominator, point.y.numerator, point.y.denominator)
        cursor_searching_points = self.connect.cursor()
        cursor_searching_points.execute(sql_smt, cond)
        search_result = []
        for point_id in cursor_searching_points:
            r = self.build_point_by_id(point_id[0])
            search_result.append(r)
            pass

        cursor_searching_points.close()
        return search_result

    def build_point_by_id(self, point_id: int) -> Point:

        if point_id in self.init_points:
            fig = self.init_figure
            point = self.init_points[point_id]
            return point

        sql_smt = 'select line1_id, line2_id from point where id = ?'
        cursor_point = self.connect.cursor()
        cursor_point.execute(sql_smt, (point_id,))
        point_node = cursor_point.fetchall()
        cursor_point.close()
        assert len(point_node) == 1
        line1_id, line2_id = point_node[0]
        line1 = self.build_line_by_id(line1_id)
        line2 = self.build_line_by_id(line2_id)
        point = line1.get_cross_point(line2)
        return point

    def build_line_by_id(self, line_id: int) -> Line:
        if line_id in self.init_lines:
            return self.init_lines[line_id]

        cursor = self.connect.cursor()
        cursor.execute("select point1_id, point2_id from line where id = ?", (line_id,))
        row = cursor.fetchall()
        cursor.close()
        assert len(row) == 1
        point1_id, point2_id = row[0]
        point1 = self.build_point_by_id(point1_id)
        point2 = self.build_point_by_id(point2_id)
        line = Line.get_line_contains_points(point1, point2)
        return line


if __name__ == '__main__':
    s = Searching()
    r = s.search_point_id_list(Point(Fraction(1, 2), Fraction(1, 2)))
    pass
