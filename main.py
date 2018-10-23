#!/usr/bin/env python3

import sys
from fractions import Fraction

import common
from draw_searching_graph import draw_result
from geo import Point
from db_for_bfs_dump_result import DBQuery, build_db


def main():
    try:
        db_query = DBQuery()
    except FileNotFoundError:  # build it
        print("the database NOT ready, building it", file=sys.stderr)
        build_db()
        db_query = DBQuery()

    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
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
