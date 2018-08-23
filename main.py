import sys, os
import fractions


class Point:
    def __init__(self, _x, _y):
        self.x = fractions.Fraction(_x)
        self.y = fractions.Fraction(_y)

    def __repr__(self):
        return '<%s, %s>' % (self.x, self.y)


class Line:
    def __init__(self, _a, _b, _c):
        self.a = _a
        self.b = _b
        self.c = _c

    def point_on(self, p):
        l = self.a * p.x + self.b * p.y - self.c
        return l == 0

    def __repr__(self):
        return '<%s * x + %s * y = %s>' % (self.a, self.b, self.c)

    def __eq__(self, other):
        det1 = det(self.a, other.a, self.b, other.b)
        if det1 != 0:
            return False
        det2 = det(self.a, self.c, other.a, other.c)
        if det2 != 0:
            return False
        return True


def line_by_2_points(p1, p2):
    a = p1.y - p2.y
    b = p2.x - p1.x
    c = p2.x * p1.y - p1.x * p2.y
    l = Line(a, b, c)
    print(l.point_on(p1))
    print(l.point_on(p2))
    return l


def det(_a, _b, _c, _d):
    return _a * _d - _b * _c


def point_by_2_lines(l1, l2):
    d = det(l1.a, l1.b, l2.a, l2.b)
    dx = det(l1.c, l1.b, l2.c, l2.b)
    dy = det(l1.a, l1.c, l2.a, l2.c)
    return Point(dx / d, dy / d)


def point_by_4_point(p1, p2, p3, p4):
    l1 = line_by_2_points(p1, p2)
    l2 = line_by_2_points(p3, p4)
    p = point_by_2_lines(l1, l2)
    return p


if __name__ == "__main__":
    half = fractions.Fraction(0.5)

    a = half + half * 3 + half * 3
    x1 = a / 3

    b = half + half + half * 3
    x2 = b / 3

    x3 = x4 = x2 + 4
    print((x1 + x2 + x3 + x4) / 4)
    print(point_by_4_point(Point(0, 0), Point(2, 2), Point(1, 1.5), Point(1.5, 0.5)))


def dfs(graph, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited


def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))


def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited


def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None


if __name__ == "__main__":
    testing_graph = {'A': set(['B', 'C']),
                  'B': set(['A', 'D', 'E']),
                  'C': set(['A', 'F']),
                  'D': set(['B']),
                  'E': set(['B', 'F']),
                  'F': set(['C', 'E'])}

    print(dfs(testing_graph, 'A'))  # {'E', 'D', 'F', 'A', 'C', 'B'
    print(list(dfs_paths(testing_graph, 'A', 'F')))
    print(bfs(testing_graph, 'A'))
    print(list(bfs_paths(testing_graph, 'A', 'F')))
    print(shortest_path(testing_graph, 'A', 'F'))