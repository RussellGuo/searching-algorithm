import os
import sqlite3
from fractions import Fraction

import common
from geo import Point


class DBCreator:
    def __init__(self, db_file_name='new_graph.db'):
        self.db_file_name = db_file_name
        try:
            os.remove(self.db_file_name)
        except FileNotFoundError:
            pass
        self.connect = sqlite3.connect(self.db_file_name)
        self.cursor_figure = self.connect.cursor()
        self.cursor_figure_line = self.connect.cursor()
        self.cursor_line = self.connect.cursor()
        self.cursor_point = self.connect.cursor()
        self.cursor_point_figure = self.connect.cursor()
        self.prepare_database()

        self.last_id_of_figure = [0]
        self.last_id_of_line = [0]
        self.last_id_of_point = [0]
        self.line_memory_table = {}  # dict which (a, b, c) => line_id
        self.point_memory_table = {}  # dict which (x_numerator, x_denominator, y_numerator, y_denominator) => point_id
        self.figure_memory_table = {}  # dict which lines => figure_id

    def prepare_database(self):
        cmd_lst = (
            "create table point(id integer,"
            " x_numerator integer, x_denominator integer, y_numerator integer, y_denominator integer)",
            "create table line(id integer, a integer, b integer, c integer)",
            "create table figure(id integer, level integer)",
            "create table figure_line(figure_id integer, line_id integer)",
            "create table point_figure(point_id integer, figure_id integer)",
        )
        self.execute_cmd_list(cmd_lst)

    def finished_database(self):
        cmd_lst = (
            "create unique index point_value_idx on point(x_numerator, x_denominator, y_numerator, y_denominator)",
            "create unique index point_primary_idx on point(id)",
            "create unique index line_primary_idx on line(id)",
            "create unique index line_value_idx on line(a, b, c)",
            "create index figure_line_idx1 on figure_line(figure_id)",
            "create index figure_line_idx2 on figure_line(line_id)",
            "create index point_figure_idx1 on point_figure(point_id)",
            "create index point_figure_idx2 on point_figure(figure_id)",
        )
        self.execute_cmd_list(cmd_lst)

    def execute_cmd_list(self, cmd_lst):
        cursor = self.connect.cursor()
        for cmd in cmd_lst:
            cursor.execute(cmd)
        cursor.close()
        self.connect.commit()

    @staticmethod
    # value is the key of dict, which should found in table_dict, maps to a id.
    # last_id_ref is a list which has only 1 int, store the last id for this table
    # return value is a tuple of id, bool, bool indicate this is a new id
    def get_index_of_memory_table_for(value, table_dict, last_id_ref):
        try:
            ret = table_dict[value], False
        except KeyError:
            last_id_ref[0] += 1
            table_dict[value] = last_id_ref[0]
            ret = table_dict[value], True
        return ret

    def get_figure_id(self, figure):
        level = len(figure)
        fig_by_line_ids = tuple(sorted([self.get_line_id(line_param) for line_param in figure]))
        id_of_figure, is_new_id = \
            DBCreator.get_index_of_memory_table_for(fig_by_line_ids,
                                                    self.figure_memory_table, self.last_id_of_figure)

        if is_new_id:
            self.cursor_figure.execute("insert into figure values(?,?)", (id_of_figure, level))
            for line_id in fig_by_line_ids:
                self.cursor_figure_line.execute("insert into figure_line values(?,?)", (id_of_figure, line_id))
        return id_of_figure

    def get_line_id(self, abc):
        id_of_line, is_new_id = DBCreator.get_index_of_memory_table_for(abc,
                                                                        self.line_memory_table, self.last_id_of_line)
        if is_new_id:
            self.cursor_line.execute("insert into line values(?,?,?,?)", (id_of_line,) + abc)
        return id_of_line

    def get_point_id(self, point):
        point_id, is_new_id = DBCreator.get_index_of_memory_table_for(point,
                                                                      self.point_memory_table, self.last_id_of_point)
        if is_new_id:
            self.cursor_point.execute("insert into point values(?,?,?,?,?)", (point_id,) + point)

        return point_id

    def save_point_figure_list_table(self, point, fig_list):
        point_id = self.get_point_id(point)
        fig_list.sort(key=len)
        assert fig_list
        first_level = len(fig_list[0])
        for fig in fig_list:
            if len(fig) != first_level:
                break
            fig_id = self.get_figure_id(fig)
            self.cursor_point_figure.execute("insert into point_figure values(?,?)", (point_id, fig_id))
        pass

    def dump_whole_table_of_point_fig_list(self, point_fig_list):
        while point_fig_list:
            point, fig_list = point_fig_list.popitem()
            ll = len(point_fig_list)
            if ll % 10000 == 0:
                print(ll)
            self.save_point_figure_list_table(point, fig_list)

    def database_commit(self):
        self.connect.commit()

        self.cursor_line.close()
        self.cursor_point.close()
        self.cursor_figure.close()
        self.cursor_figure_line.close()
        self.cursor_point_figure.close()

        self.finished_database()


class DBQuery:
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
                fig0 = common.apply_mat_on_figure(fig, common.inv_for_symmetry_mat(mat))
                result.append(tuple(fig0))
        result = list(set(result))
        result.sort()
        return result


if __name__ == '__main__':
    from common import get_cached_pythagorea_graph

    db = DBCreator()
    point_fig_list = get_cached_pythagorea_graph()
    db.dump_whole_table_of_point_fig_list(point_fig_list)
    db.database_commit()
    pass
