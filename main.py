#!/usr/bin/env python3
# -*- coding: utf8 -*-

import itertools
import sys
from fractions import Fraction

import common
from db_for_bfs_dump_result import DBQuery, build_db
from draw_searching_graph import draw_resolution
from geo import Point, Line
from tan_arith import tan_of_complementary, tan_of_add, tan_of_neg, tan_of_double, tan_of_sub


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


def question_14_9(query):
    # get Point B
    line1 = Line.get_line_contains_points(Point(-3, 1), Point(3, 3))
    line2 = Line(1, 0, -2)
    B = line1.get_cross_point(line2)
    # get Point A
    line1 = Line.get_line_contains_points(Point(2, -3), Point(3, 0))
    line2 = Line(0, 1, -1)
    A = line1.get_cross_point(line2)
    del line1, line2

    # get the midpoint
    target_point_x = (A.x + B.x) / 2
    target_point_y = (A.y + B.y) / 2
    point_target = Point(target_point_x, target_point_y, "Target")

    # query and show it(them)
    solution = query.query_point_by_symmetry(point_target)
    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    for r in solution:
        draw_resolution(r, [point_target], init_figure, grid_size)


def question_14_8(query):
    # get Point B
    line1 = Line.get_line_contains_points(Point(-3, -1), Point(3, -3))
    line2 = Line(1, 0, -2)
    B = line1.get_cross_point(line2)
    # get Point A
    line1 = Line.get_line_contains_points(Point(-3, 1), Point(2, 2))
    line2 = Line(1, 0, 1)
    A = line1.get_cross_point(line2)
    del line1, line2

    point_target = A.middle(B)

    # query and show it(them)
    solution = query.query_point_by_symmetry(point_target)
    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    for r in solution:
        draw_resolution(r, [point_target], init_figure, grid_size)


def question_16_12(query):
    line1 = Line.get_line_contains_points(Point(-2, 0), Point(1, -1))
    line2 = Line.get_line_contains_points(Point(0, 3), Point(1, 0))
    line = Line.get_bisectors_for_2lines(line1, line2)[1]
    A = line1.get_cross_point(line2)

    # query and show it(them)
    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    init_figure.extend(((line1.a, line1.b, line1.c), (line2.a, line2.b, line2.c)))
    solution = query.query_line_by_symmetry(line, (A,), init_figure)

    points = set([s[0] for s in solution])
    for r in solution[:4]:
        p, fig = r
        draw_resolution(fig, points, init_figure, grid_size)


def question_16_15(query):
    line1 = Line.get_line_contains_points(Point(-2, 0), Point(0, 1))
    line2 = Line.get_line_contains_points(Point(0, -1), Point(1, 1))
    line = Line.get_bisectors_for_2lines(line1, line2)[0]
    A = line1.get_cross_point(line2)

    # query and show it(them)
    solution = query.query_line_by_symmetry(line, (A,))
    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    init_figure.extend(((line1.a, line1.b, line1.c), (line2.a, line2.b, line2.c)))

    points = set([s[0] for s in solution])
    for r in solution[:4]:
        p, fig = r
        draw_resolution(fig, points, init_figure, grid_size)


def question_24_6(query):
    A = Point(1, -2)
    B = Point(0, 1)
    line1 = Line.get_line_contains_points(A, B)
    line2 = Line.get_line_by_point_slope(A, Fraction(4))

    tan_alpha = Fraction(1, 4)
    tan_beta = Fraction(1, 3)
    tan_theta = tan_of_add(tan_of_double(tan_beta), tan_alpha)
    slope = tan_of_neg(tan_of_complementary(tan_theta))

    line = Line.get_line_by_point_slope(A, slope)
    # query and show it(them)
    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    init_figure.extend(((line1.a, line1.b, line1.c), (line2.a, line2.b, line2.c)))
    solution = query.query_line_by_symmetry(line, (A,), init_figure)

    points = set([s[0] for s in solution])
    for r in solution[:4]:
        p, fig = r
        draw_resolution(fig, points, init_figure, grid_size)


def question_24_7(query):
    A = Point(2, -1)
    B = Point(-2, 0)
    line1 = Line.get_line_contains_points(A, B)
    line2 = Line.get_line_by_point_slope(A, Fraction(-1))

    tan_alpha = Fraction(1, 4)
    tan_beta = tan_of_sub(Fraction(1), tan_alpha)
    tan_theta = tan_of_sub(tan_beta, tan_alpha)
    slope = tan_theta

    line = Line.get_line_by_point_slope(A, slope)
    # query and show it(them)
    init_figure, grid_size = common.INIT_FIGURE(), common.GRID_SIZE()
    init_figure.extend(((line1.a, line1.b, line1.c), (line2.a, line2.b, line2.c)))
    solution = query.query_line_by_symmetry(line, (A,), init_figure)

    points = set([s[0] for s in solution])

    for r in solution[:4]:
        p, fig = r
        draw_resolution(fig, points, init_figure, grid_size)


def main():
    db_query = get_query_obj()
    # question_22_17(db_query)
    # question_27_14(db_query)
    # question_27_15(db_query)
    # question_14_9(db_query)
    # question_14_8(db_query)
    # question_16_15(db_query)
    question_16_12(db_query)
    # question_24_6(db_query)
    # question_24_7(db_query)


if __name__ == '__main__':
    main()
