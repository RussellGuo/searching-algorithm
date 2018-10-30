#!/usr/bin/env python3
# -*- coding: utf8 -*-

import itertools
import sys
from fractions import Fraction

import common
from db_for_bfs_dump_result import DBQuery, build_db
from draw_searching_graph import draw_resolution
from geo import Point, Line


def get_query_obj() -> DBQuery:
    try:
        db_query = DBQuery()
    except FileNotFoundError:  # build it
        print("the database NOT ready, building it", file=sys.stderr)
        build_db()
        db_query = DBQuery()
    return db_query


def exam_22_17(query):
    VertexB = Point(Fraction(1), Fraction(-2), "B")
    VertexC = Point(Fraction(-2), Fraction(-1), "C")
    EdgeA = Line.get_line_contains_points(VertexB, VertexC)
    p1 = Point(Fraction(2), Fraction(0), "p1")
    p2 = Point(Fraction(2), Fraction(1), "p2")
    EdgeC = Line.get_line_contains_points(VertexB, p1)
    EdgeB = Line.get_line_contains_points(VertexC, p2)
    del p1, p2

    BisectorAngleA = Line.get_bisectors_for_2lines(EdgeB, EdgeC)[0]
    VertexOfTargetDiamondInsideEdgeA = EdgeA.get_cross_point(BisectorAngleA)

    EageOfTargetDiamondParallelsToEdgeC = Line.get_line_parallel_to(EdgeC, VertexOfTargetDiamondInsideEdgeA)
    EageOfTargetDiamondParallelsToEdgeB = Line.get_line_parallel_to(EdgeB, VertexOfTargetDiamondInsideEdgeA)
    VertexOfTargetDiamondInsideEdgeB = Line.get_cross_point(EageOfTargetDiamondParallelsToEdgeC, EdgeB)
    VertexOfTargetDiamondInsideEdgeC = Line.get_cross_point(EageOfTargetDiamondParallelsToEdgeB, EdgeC)

    resolution_vertex_in_edge_a = query.query_point_by_symmetry(VertexOfTargetDiamondInsideEdgeA)
    resolution_vertex_in_edge_b = query.query_point_by_symmetry(VertexOfTargetDiamondInsideEdgeB)
    resolution_vertex_in_edge_c = query.query_point_by_symmetry(VertexOfTargetDiamondInsideEdgeC)

    TriangleEdges = {(EdgeA.a, EdgeA.b, EdgeA.c), (EdgeB.a, EdgeB.b, EdgeB.c), (EdgeC.a, EdgeC.b, EdgeC.c)}
    resolution_product = itertools.product(resolution_vertex_in_edge_a,
                                           resolution_vertex_in_edge_b,
                                           resolution_vertex_in_edge_c)
    resolution_for_all = [frozenset((set(r[0]) | set(r[1]) | set(r[2])) - TriangleEdges) for r in resolution_product]
    resolution_for_all.sort()

    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    init_figure.extend(TriangleEdges)
    targets = (VertexOfTargetDiamondInsideEdgeC, VertexOfTargetDiamondInsideEdgeB, VertexOfTargetDiamondInsideEdgeA)
    for r in resolution_for_all:
        draw_resolution(r, targets, init_figure, grid_size)


def main():
    db_query = get_query_obj()
    exam_22_17(db_query)


if __name__ == '__main__':
    main()
