from collections import deque
import heapq
from enchaminhamento import aux_get
import math


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
            edge_cost = aux_get(graph[start][neighbor])["length"]
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
                cost = sum(aux_get(graph[path[i]][path[i + 1]])["length"] for i in range(len(path) - 1))
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
                edge_cost = aux_get(graph[start][neighbor])["length"]
                updated_cost = cost + edge_cost
                result = dfs_limit(graph, neighbor, end, depth - 1, visited, updated_cost, path, visited_list)
                if result:
                    return result

    return None


def bidirectional(graph, start_node, end_node):
    if start_node == end_node:
        return [], [start_node], 0

    forward_queue = [start_node]
    backward_queue = [end_node]

    forward_visited = set()
    backward_visited = set()

    forward_parent = {start_node: None}
    backward_parent = {end_node: None}

    intersection_node = None

    while forward_queue and backward_queue:
        # Perform forward search
        current_node = forward_queue.pop(0)
        forward_visited.add(current_node)

        for neighbor in graph.neighbors(current_node):
            if neighbor not in forward_visited:
                forward_queue.append(neighbor)
                forward_parent[neighbor] = current_node

            if neighbor in backward_visited:
                intersection_node = neighbor
                break

        if intersection_node:
            break

        # Perform backward search
        current_node = backward_queue.pop(0)
        backward_visited.add(current_node)

        for neighbor in graph.neighbors(current_node):
            if neighbor not in backward_visited:
                backward_queue.append(neighbor)
                backward_parent[neighbor] = current_node

            if neighbor in forward_visited:
                intersection_node = neighbor
                break

        if intersection_node:
            break

    if intersection_node is None:
        return [], [], 0  # No path found

    # Reconstruct the path from start to end
    path = []
    current_node = intersection_node
    while current_node is not None:
        path.insert(0, current_node)
        current_node = forward_parent[current_node]

    # Reconstruct the path from end to start
    current_node = backward_parent[intersection_node]
    while current_node is not None:
        path.append(current_node)
        current_node = backward_parent[current_node]

    return [], path, 0

def calculate_euclidean_distance_partial(lat1, lon1, x2, y2, z2):
    R = 6371  # Raio do planeta

    x1 = R * math.cos(lat1) * math.cos(lon1)
    y1 = R * math.cos(lat1) * math.sin(lon1)
    z1 = R * math.sin(lat1)

    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2) + math.pow((z2 - z1), 2))

def calculate_heuristics(graph, node):
    heuristics = {node: 0}
    nodes = graph.nodes(data=True)
    n_lat = nodes[node]['x']
    n_lon = nodes[node]['y']
    R = 6371  # Raio do planeta
    x2 = R * math.cos(n_lat) * math.cos(n_lon)
    y2 = R * math.cos(n_lat) * math.sin(n_lon)
    z2 = R * math.sin(n_lat)

    for n, coord in nodes:
        if n != node:
            heuristics[n] = calculate_euclidean_distance_partial(coord['x'], coord['y'], x2, y2, z2)

    return heuristics


def greedy_search(graph, start_node, goal_node):
    heuristics = calculate_heuristics(graph, goal_node)
    # Priority queue to store nodes based on heuristic values
    priority_queue = [(heuristics[start_node], start_node, [start_node])]
    visited = set()

    while priority_queue:
        # Get the node with the minimum heuristic value and its path
        current_heuristic, current_node, path = priority_queue.pop(0)

        # Check if the goal node is reached
        if current_node == goal_node:
            return [], path, 0

        # Mark the current node as visited
        visited.add(current_node)

        # Explore neighbors
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                # Add neighbors to the priority queue based on heuristic values
                new_path = path + [neighbor]
                priority_queue.append((heuristics[neighbor], neighbor, new_path))
                priority_queue.sort()  # Sort based on heuristic values

    return [], [], 0

def astar_search(graph, start_node, goal_node):
    heuristics = calculate_heuristics(graph, goal_node)
    # Priority queue to store nodes based on the total cost (f-value)
    priority_queue = [(heuristics[start_node], 0, start_node, [start_node])]
    visited = set()

    while priority_queue:
        # Get the node with the minimum total cost (f-value) and its path
        current_heuristic, current_cost, current_node, path = priority_queue.pop(0)

        # Check if the goal node is reached
        if current_node == goal_node:
            return [], path, 0

        # Mark the current node as visited
        visited.add(current_node)

        # Explore neighbors
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                # Calculate the cost for the neighbor node
                edge_data = aux_get(graph[current_node][neighbor])
                edge_length = edge_data['length'] if edge_data else 0
                neighbor_cost = current_cost + edge_length

                # Calculate the total cost (f-value) for the neighbor
                total_cost = neighbor_cost + heuristics[neighbor]

                # Add neighbors to the priority queue based on total cost
                new_path = path + [neighbor]
                priority_queue.append((total_cost, neighbor_cost, neighbor, new_path))
                priority_queue.sort()  # Sort based on total cost

    print(f"Goal node {goal_node} not reachable from {start_node}")
    return [], [], 0