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
        self.line_memory_table = {}
        self.point_memory_table = {}

    def prepare_database(self):
        cmd_lst = (
            "create table point(id integer,"
            " x_numerator integer, x_denominator integer, y_numerator integer, y_denominator integer)",
            "create table line(id integer, a integer, b integer, c integer)",
            "create table figure(id integer, level integer)",
            "create table figure_line(figure_id integer, line_id integer)",
            "create table point_figure(point_id integer, figure_id integer)",
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

        # self.connect.commit()

    def get_line_id_by_param(self, abc):
        if abc in self.line_memory_table:
            return self.line_memory_table[abc]

        self.last_id_of_line += 1
        id_of_line = self.last_id_of_line
        self.line_memory_table[abc] = id_of_line
        cursor = self.connect.cursor()
        cursor.execute("insert into line values(?,?,?,?)", (id_of_line,) + abc)
        cursor.close()
        return id_of_line

    def save_into_figure_line_table(self, fig_id: int, line_id: int):
        cursor = self.connect.cursor()
        cursor.execute("insert into figure_line values(?,?)", (fig_id, line_id))
        cursor.close()

    def save_into_point_table_etc(self, fig_id: int, fig_level: int, point: Point):
        point_vector = (point.x.numerator, point.x.denominator, point.y.numerator, point.y.denominator)

        # find point_id
        if point_vector in self.point_memory_table:
            point_id, level = self.point_memory_table[point_vector]
            if level < fig_level:
                return # no need to save this point into point_figure table
        else:
            self.last_id_of_point += 1
            point_id = self.last_id_of_point
            self.point_memory_table[point_vector] = (point_id, fig_level)
            cursor = self.connect.cursor()
            cursor.execute("insert into point values(?,?,?,?,?)",
                           (point_id,) + point_vector)
            cursor.close()

        # update point_figure table
        # should added the connection table for figure
        cursor = self.connect.cursor()
        cursor.execute("insert into point_figure values(?,?)", (point_id, fig_id))
        cursor.close()


def main():
    db_creator = NewDBCreator()

    i = 0
    for figure_params in bin_figure_iter():
        db_creator.append_figure_by_params_of_lines(figure_params)
        i += 1
        if i % 10000 == 0:
            print(i)


if __name__ == '__main__':
    main()
