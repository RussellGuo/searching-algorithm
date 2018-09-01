import os
import sqlite3


def covert():
    db_file_name = 'graph.db'
    try:
        os.remove(db_file_name)
    except FileNotFoundError:
        pass

    connect = sqlite3.connect(db_file_name)
    cursor = connect.cursor()
    cursor.execute("create table figure (id integer, parent_id integer, line_id integer)")
    cursor.execute("create table line   (id integer, a integer, b integer, c integer, point1_id, point2_id)")
    cursor.execute("create table point  (id integer, " +
                   "x_numerator integer, x_denominator integer, y_numerator integer, y_denominator integer, " +
                   "line1_id integer, line2_id integer)")

    with open("graph.txt") as f:
        table_name_dict = {2: "figure", 5: "line", 6: "point"}
        for one_line in f:
            if one_line[0] != '(':
                continue
            line = one_line.strip()
            cnt = line.count(',')
            table_name = table_name_dict[cnt]
            sql_cmd = 'insert into %s values%s' % (table_name, line)
            cursor.execute(sql_cmd)

    cursor.close()
    connect.commit()
    connect.close()


if __name__ == '__main__':
    covert()
