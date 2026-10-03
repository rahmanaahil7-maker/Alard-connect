import heapq
import time

def get_effective_weight(edge, preferences):
    w = edge["weight"]
    if "wheelchair" in preferences and edge.get("has_stairs"): w += 1000
    if "avoid_stairs" in preferences and edge.get("has_stairs"): w += 500
    if "avoid_crowds" in preferences and edge.get("is_crowded"): w += 300
    if "prefer_covered" in preferences and not edge.get("is_covered"): w += 100
    return w

def dijkstra_shortest_path(graph, start, end, preferences):
    start_time = time.perf_counter()
    pq = [(0, start)]
    distances = {node: float('inf') for node in graph.adjacency_list}
    distances[start] = 0
    previous_nodes = {node: None for node in graph.adjacency_list}
    nodes_explored = 0

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        nodes_explored += 1
        
        if current_distance > distances[current_node]: continue
        if current_node == end: break

        for edge in graph.adjacency_list[current_node]:
            neighbor = edge["node"]
            weight = get_effective_weight(edge, preferences)
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    path, curr = [], end
    while curr is not None:
        path.insert(0, curr)
        curr = previous_nodes.get(curr)
        
    exec_time = (time.perf_counter() - start_time) * 1000
    if not path or path[0] != start: return None, float('inf'), nodes_explored, exec_time
    return path, distances[end], nodes_explored, exec_time