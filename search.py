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
        for nxt in graph[vertex] - set(path):
            new = path + [nxt]
            if nxt == goal:
                yield new
            else:
                stack.append((nxt, new))


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
        for nxt in graph[vertex] - set(path):
            new = path + [nxt]
            if nxt == goal:
                yield new
            else:
                queue.append((nxt, new))


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
