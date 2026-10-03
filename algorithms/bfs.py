from collections import deque
import time

def get_effective_weight(edge, preferences):
    w = edge["weight"]
    if "wheelchair" in preferences and edge.get("has_stairs"): w += 1000
    if "avoid_stairs" in preferences and edge.get("has_stairs"): w += 500
    if "avoid_crowds" in preferences and edge.get("is_crowded"): w += 300
    if "prefer_covered" in preferences and not edge.get("is_covered"): w += 100
    return w

def bfs_fewest_edges_path(graph, start, end, preferences):
    start_time = time.perf_counter()
    queue = deque([(start, [start], 0)])
    visited = {start}
    nodes_explored = 0

    while queue:
        current_node, path, current_dist = queue.popleft()
        nodes_explored += 1
        
        if current_node == end:
            exec_time = (time.perf_counter() - start_time) * 1000
            return path, current_dist, nodes_explored, exec_time

        for edge in graph.adjacency_list.get(current_node, []):
            neighbor = edge["node"]
            weight = get_effective_weight(edge, preferences)
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], current_dist + weight))
                
    exec_time = (time.perf_counter() - start_time) * 1000
    return None, float('inf'), nodes_explored, exec_time