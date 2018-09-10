import array
import os
import sqlite3

from figure import Figure
from geo import Point


def bin_figure_iter():
    max_depth = 3
    for dep in range(max_depth):
        no = dep + 1
        with open("figure-level%d.bin" % no, "rb") as f:
            while True:
                bin_record = array.array("h")
                try:
                    bin_record.fromfile(f, no * 3)
                except EOFError:
                    break
                a = bin_record.tolist()
                vv = []
                for i in range(no):
                    v = a[i * 3:(i + 1) * 3]
                    vv.append(tuple(v))
                yield vv


class NewDBCreator:
    db_file_name = 'new_graph.db'

    def __init__(self):
        self.db_file_name = NewDBCreator.db_file_name
        try:
            os.remove(self.db_file_name)
        except FileNotFoundError:
            pass
        self.connect = sqlite3.connect(self.db_file_name)
        self.prepare_database()

        self.last_id_of_figure = self.last_id_of_line = self.last_id_of_point = 0

    def prepare_database(self):
        cmd_lst = (
            "create table point(id integer primary key,"
            " x_numerator integer, x_denominator integer, y_numerator integer, y_denominator integer)",
            "create unique index point_value_idx on point(x_numerator, x_denominator, y_numerator, y_denominator)",
            "create table line(id integer primary key, a integer, b integer, c integer)",
            "create unique index line_value_idx on line(a, b, c)",
            "create table figure(id integer primary key, level integer)",
            "create table figure_line(figure_id integer, line_id integer)",
            "create index figure_line_idx on figure_line(figure_id)",
            "create table point_figure(point_id integer, figure_id integer)",
            "create index point_figure_idx1 on point_figure(point_id)",
            "create index point_figure_idx2 on point_figure(figure_id)",
        )
        cursor = self.connect.cursor()
        for cmd in cmd_lst:
            cursor.execute(cmd)
        cursor.close()
        self.connect.commit()

    def append_figure_by_params_of_lines(self, figure_params):
        level = len(figure_params)
        self.last_id_of_figure += 1
        id_of_figure = self.last_id_of_figure
        cursor = self.connect.cursor()
        cursor.execute("insert into figure values(?,?)", (id_of_figure, level))
        cursor.close()

        for line_param in figure_params:
            line_id = self.get_line_id_by_param(line_param)
            # save into figure-line table
            self.save_into_figure_line_table(id_of_figure, line_id)

        fig = Figure.build_figure_by_params_of_lines(figure_params)
        for p in fig.new_points:
            self.save_into_point_table_etc(id_of_figure, level, p)

        self.connect.commit()

    def get_line_id_by_param(self, abc):
        cursor = self.connect.cursor()
        cursor.execute("select id from line where a = ? and b = ? and c = ?", abc)
        row = cursor.fetchall()
        cursor.close()

        if len(row) == 1:
            return row[0][0]
        if len(row) != 0:
            assert False
        self.last_id_of_line += 1
        id_of_line = self.last_id_of_line
        cursor = self.connect.cursor()
        cursor.execute("insert into line values(?,?,?,?)", (id_of_line,) + abc)
        cursor.close()
        return id_of_line

    def save_into_figure_line_table(self, fig_id: int, line_id: int):
        cursor = self.connect.cursor()
        cursor.execute("insert into figure_line values(?,?)", (fig_id, line_id))
        cursor.close()

    def save_into_point_table_etc(self, fig_id: int, fig_level: int, point: Point):
        x_numerator, x_denominator, y_numerator, y_denominator = \
            point.x.numerator, point.x.denominator, point.y.numerator, point.y.denominator

        # find point_id
        cursor = self.connect.cursor()
        cursor.execute(
            "select id from point where x_numerator = ? and x_denominator = ? and y_numerator = ? and y_denominator = ?",
            (x_numerator, x_denominator, y_numerator, y_denominator))
        row = cursor.fetchall()
        cursor.close()
        assert len(row) <= 1
        exists_in_table_before = len(row) == 1

        if exists_in_table_before:
            point_id = row[0][0]

            # let check if this point is generated at lower figure
            cursor = self.connect.cursor()
            cursor.execute(
                "select 1 from point_figure, figure where"
                " point_figure.point_id = ? and figure.id = point_figure.figure_id and figure.level < ?",
                (point_id, fig_level))
            exists_at_lower_figure = cursor.fetchone() is not None
            if exists_at_lower_figure:
                pass
            cursor.close()

        else:
            self.last_id_of_point += 1
            point_id = self.last_id_of_point
            cursor = self.connect.cursor()
            cursor.execute("insert into point values(?,?,?,?,?)",
                           (point_id, x_numerator, x_denominator, y_numerator, y_denominator))
            cursor.close()
            exists_at_lower_figure = False  # because it's a new point

        # update point_figure table
        if not exists_at_lower_figure:
            # should added the connection table for figure
            cursor = self.connect.cursor()
            cursor.execute("insert into point_figure values(?,?)", (point_id, fig_id))
            cursor.close()


def main():
    db_creator = NewDBCreator()

    for figure_params in bin_figure_iter():
        db_creator.append_figure_by_params_of_lines(figure_params)


if __name__ == '__main__':
    main()
