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


def question_22_17(query):
    VertexB = Point(Fraction(1), Fraction(-2), "B")
    VertexC = Point(Fraction(-2), Fraction(-1), "C")
    EdgeA = Line.get_line_contains_points(VertexB, VertexC)
    p1 = Point(Fraction(2), Fraction(0), "p1")
    p2 = Point(Fraction(2), Fraction(1), "p2")
    EdgeC = Line.get_line_contains_points(VertexB, p1)
    EdgeB = Line.get_line_contains_points(VertexC, p2)
    del p1, p2

    BisectorAngleA = Line.get_bisectors_for_2lines(EdgeB, EdgeC)[0]
    VertexOfTargetRhombusInsideEdgeA = EdgeA.get_cross_point(BisectorAngleA)

    EageOfTargetRhombusParallelsToEdgeC = Line.get_line_parallel_to(EdgeC, VertexOfTargetRhombusInsideEdgeA)
    EageOfTargetRhombusParallelsToEdgeB = Line.get_line_parallel_to(EdgeB, VertexOfTargetRhombusInsideEdgeA)
    VertexOfTargetRhombusInsideEdgeB = Line.get_cross_point(EageOfTargetRhombusParallelsToEdgeC, EdgeB)
    VertexOfTargetRhombusInsideEdgeC = Line.get_cross_point(EageOfTargetRhombusParallelsToEdgeB, EdgeC)

    resolution_vertex_in_edge_a = query.query_point_by_symmetry(VertexOfTargetRhombusInsideEdgeA)
    resolution_vertex_in_edge_b = query.query_point_by_symmetry(VertexOfTargetRhombusInsideEdgeB)
    resolution_vertex_in_edge_c = query.query_point_by_symmetry(VertexOfTargetRhombusInsideEdgeC)

    TriangleEdges = {(EdgeA.a, EdgeA.b, EdgeA.c), (EdgeB.a, EdgeB.b, EdgeB.c), (EdgeC.a, EdgeC.b, EdgeC.c)}
    resolution_product = itertools.product(resolution_vertex_in_edge_a,
                                           resolution_vertex_in_edge_b,
                                           resolution_vertex_in_edge_c)
    solution_for_all = [frozenset((set(r[0]) | set(r[1]) | set(r[2])) - TriangleEdges) for r in resolution_product]
    solution_for_all.sort()

    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    init_figure.extend(TriangleEdges)
    targets = (VertexOfTargetRhombusInsideEdgeA, VertexOfTargetRhombusInsideEdgeB, VertexOfTargetRhombusInsideEdgeC)
    for r in solution_for_all:
        draw_resolution(r, targets, init_figure, grid_size)


# grid_mask is a boolean sequence of top-left, top-right, bottom-left, bottom-right
def centroid_of_2x2_grid(center_x, center_y, grid_mask):
    one_half = Fraction(1, 2)
    count = 0
    sum_x = sum_y = Fraction(0)
    deta_grid_coord = (-one_half, +one_half), (+one_half, +one_half), (-one_half, -one_half), (one_half, -one_half)
    for grid_value, deta in zip(grid_mask, deta_grid_coord):
        if grid_value:
            count += 1
            sum_x += center_x + deta[0]
            sum_y += center_y + deta[1]
    return sum_x / count, sum_y / count, count


def centroid_of_iter(it):
    sum_weight = 0
    sum_x = sum_y = Fraction(0)
    for x, y, weight in it:
        sum_x += x * weight
        sum_y += y * weight
        sum_weight += weight
    return sum_x / sum_weight, sum_y / sum_weight, sum_weight


def question_27_14(query):
    total = []
    total.append(centroid_of_2x2_grid(-2, +2, (True, True, True, False)))
    total.append(centroid_of_2x2_grid(+2, +2, (True, True, False, True)))
    total.append(centroid_of_2x2_grid(-2, -2, (True, False, True, True)))
    total.append(centroid_of_2x2_grid(+2, -2, (True, True, True, False)))
    x, y, w = centroid_of_iter(total)
    point_target = Point(x, y, "Target")
    solution = query.query_point_by_symmetry(point_target)
    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    for r in solution:
        draw_resolution(r, [point_target], init_figure, grid_size)


def question_27_15(query):
    total = []
    total.append((Fraction(-1.5), Fraction(1.5), 4))  # top-left
    total.append((2, Fraction(1.5), 4))  # top-right

    total.append((centroid_of_2x2_grid(-2, -2, (False, True, True, True))))  # bottom-left -very left
    total.append((centroid_of_2x2_grid(0, -2, (False, False, True, False))))  # bottom-left -right part

    total.append((2, -2, 4))  # bottom-right
    x, y, w = centroid_of_iter(total)
    point_target = Point(x, y, "Target")
    solution = query.query_point_by_symmetry(point_target)
    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    for r in solution:
        draw_resolution(r, [point_target], init_figure, grid_size)


def main():
    db_query = get_query_obj()
    # question_22_17(db_query)
    # question_27_14(db_query)
    question_27_15(db_query)


if __name__ == '__main__':
    main()
