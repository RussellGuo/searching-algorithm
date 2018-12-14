import sqlite3
from fractions import Fraction

from geo import Point

connect = sqlite3.connect("file:" + "full.db" + "?mode=ro", uri=True)
cursor_fig = connect.cursor()
cursor_line = connect.cursor()
cursor_point = connect.cursor()

cursor_fig.execute("select id from figure")

for fig_id_row in cursor_fig:
    fig_id = fig_id_row[0]
    cursor_line.execute("select a, b, c from line, figure_line where figure_id = ? and line_id = line.id", (fig_id,))
    lines_row = cursor_line.fetchall()
    lines_row.sort()
    for line in lines_row:
        print(line[0], line[1], line[2], end=' ')
    print(0, 0, 0, end=' ')
    cursor_point.execute(
        "select x_numerator, x_denominator, y_numerator, y_denominator from point, point_figure "
        "where point_id = point.id and figure_id = ?",
        (fig_id,))
    point_rows = cursor_point.fetchall()
    point_rows.sort(key=lambda p: Point(Fraction(p[0], p[1]), Fraction(p[2], p[3])))
    for point in point_rows:
        print(point[0], point[1], point[2], point[3], end=' ')
    print(0, 0, 0, 0)
    pass
