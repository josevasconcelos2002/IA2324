from collections import deque
import heapq
from enchaminhamento import aux_get


def dfs(graph, start, end, visited=None, cost=0, path=None, visited_list=[]):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    visited_list.append(start)
    path = path + [start]

    if start == end:
        return visited_list, path, round(cost, 2)

    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            edge_cost = graph[start][neighbor]["length"]
            updated_cost = cost + edge_cost
            result = dfs(graph, neighbor, end, visited, updated_cost, path, visited_list)
            if result:
                return result

    return None


def bfs(graph, start, end):
    visited = set()
    visited_list = []
    queue = deque([(start, [])])

    while queue:
        current_node, path = queue.popleft()

        if current_node not in visited:
            visited.add(current_node)
            visited_list.append(current_node)
            path = path + [current_node]

            if current_node == end:
                # Calculate the sum of edge costs along the path
                cost = sum(graph[path[i]][path[i + 1]]["length"] for i in range(len(path) - 1))
                return visited_list, path, round(cost, 2)

            neighbors = graph[current_node]
            queue.extend((neighbor, path) for neighbor in neighbors if neighbor not in visited)

    return None


def dijkstra(graph, start, end):
    lengths = {node: float('inf') for node in graph}
    lengths[start] = 0

    priority_queue = [(0, start)]
    visited = []

    while priority_queue:
        current_length, current_node = heapq.heappop(priority_queue)

        if current_length > lengths[current_node]:
            continue

        visited.append(current_node)

        for neighbor, edge_data in graph[current_node].items():
            edge_cost = aux_get(edge_data)["length"]
            total_cost = current_length + edge_cost

            if total_cost < lengths[neighbor]:
                lengths[neighbor] = total_cost
                heapq.heappush(priority_queue, (total_cost, neighbor))

    path = []
    current = end
    while current != start:
        path.insert(0, current)
        current = min((node for node in graph[current] if
                       lengths[node] + aux_get(graph[current][node])["length"] == lengths[current]),
                      key=lambda x: aux_get(graph[current][x])["length"])

    path.insert(0, start)

    return visited, path, round(lengths[end], 2)


def iddfs(graph, start, end, max_depth=2**31-1):
    for depth in range(max_depth + 1):
        result = dfs_limit(graph, start, end, depth)
        if result:
            if result[1]:
                return result[0], result[1], round(result[2], 2)
    return None


def dfs_limit(graph, start, end, depth, visited=None, cost=0, path=None, visited_list=[]):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    visited_list.append(start)
    path = path + [start]

    if start == end:
        return visited_list, path, round(cost, 2)

    if depth > 0:
        for neighbor in graph.neighbors(start):
            if neighbor not in visited:
                edge_cost = graph[start][neighbor]["length"]
                updated_cost = cost + edge_cost
                result = dfs_limit(graph, neighbor, end, depth - 1, visited, updated_cost, path, visited_list)
                if result:
                    return result

    return None


def bidirectional(graph, start, goal):
    forward_visited = []
    backward_visited = []
    forward_queue = deque([(start, [], 0)])
    backward_queue = deque([(goal, [], 0)])

    while forward_queue or backward_queue:
        if forward_queue:
            forward_node, forward_path, cost = forward_queue.popleft()

            if forward_node not in forward_visited:
                forward_visited.append(forward_node)
                forward_path.append(forward_node)
#TODO: ISTO ESTÁ UMA CAGADA. É PRECISO ARRANJAR MANEIRA DE IR BUSCAR O CAMINHO AO BACKWARD_QUEUE. NAO SE PODE USAR O BFS
                if forward_node == goal or forward_node in backward_visited:
                    intersection_node = forward_node if forward_node in backward_visited else None
                    _, b_path, b_cost = bfs(graph, intersection_node, goal)
                    b_path.pop(0)
                    path = forward_path + b_path
                    return forward_visited + backward_visited, path, round(cost + b_cost, 2)

                forward_neighbors = graph[forward_node]
                forward_queue.extend((neighbor, forward_path.copy(), cost + graph[forward_node][neighbor]['length']) for neighbor in forward_neighbors if neighbor not in forward_visited)

        if backward_queue:
            backward_node, backward_path, cost = backward_queue.popleft()

            if backward_node not in backward_visited:
                backward_visited.append(backward_node)
                backward_path = [backward_node] + backward_path
#TODO: ESTE NÃO ESTÁ FEITO AINDA. FAZER ALTERAÇÕES PARECIDAS COM O DE CIMA E TESTAR
                if backward_node == start or backward_node in forward_visited:
                    intersection_node = backward_node if backward_node in forward_visited else None
                    print(f"Int Node Back: {intersection_node}")
                    print(f"For: {forward_visited}"
                          f"Back: {backward_visited}")
                    i = forward_path.index(intersection_node)
                    path = forward_path[:i+1] + backward_path[:i][::-1]
                    return forward_visited + backward_visited, path, cost

                backward_neighbors = graph[backward_node]
                backward_queue.extend((neighbor, backward_path.copy(), cost + graph[backward_node][neighbor]['length']) for neighbor in backward_neighbors if neighbor not in backward_visited)

    return None
