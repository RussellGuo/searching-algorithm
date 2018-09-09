import array
import os
import sqlite3


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

    def prepare_database(self):
        cmds = (
            "create table point(id integer primary key,"
            " x_numerator integer, x_denominator integer, y_numerator integer, y_denominator integer)",
            "create unique index point_value_idx on point(x_numerator, x_denominator, y_numerator, y_denominator)",
            "create table line(id integer primary key, a integer, b integer, c integer)",
            "create unique index line_value_idx on line(a, b, c)",
            "create table figure(id integer primary key, line_count integer, point_count integer)",
            "create table figure_line(figure_id integer, line_id integer)",
            "create index figure_line_idx on figure_line(figure_id)",
            "create table point_figure(point_id integer, figure_id integer)",
            "create index point_figure_idx on point_figure(point_id)",
        )
        cursor = self.connect.cursor()
        for cmd in cmds:
            cursor.execute(cmd)
        cursor.close()
        self.connect.commit()

    def append_figure(self, params_of_lines):
        pass


def main():
    db_creator = NewDBCreator()
    for figure_params in bin_figure_iter():
        db_creator.append_figure(figure_params)

if __name__ == '__main__':
    main()