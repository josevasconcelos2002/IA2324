from collections import deque
import heapq


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
            edge_cost = graph[start][neighbor]["distance"]
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
                cost = sum(graph[path[i]][path[i + 1]]["distance"] for i in range(len(path) - 1))
                return visited_list, path, cost

            neighbors = graph[current_node]
            queue.extend((neighbor, path) for neighbor in neighbors if neighbor not in visited)

    return None


def custo_uniforme(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    priority_queue = [(0, start)]
    visited = []

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        visited.append(current_node)

        for neighbor, edge_data in graph[current_node].items():
            edge_cost = edge_data["distance"]
            total_cost = current_distance + edge_cost

            if total_cost < distances[neighbor]:
                distances[neighbor] = total_cost
                heapq.heappush(priority_queue, (total_cost, neighbor))

    path = []
    current = end
    while current != start:
        path.insert(0, current)
        current = min((node for node in graph[current] if
                       distances[node] + graph[current][node]["distance"] == distances[current]),
                      key=lambda x: graph[current][x]["distance"])

    path.insert(0, start)

    return visited, path, round(distances[end], 2)
