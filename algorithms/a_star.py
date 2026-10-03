import heapq
import time
import math

def heuristic(node1, node2):
    return math.sqrt((node1['x'] - node2['x'])**2 + (node1['y'] - node2['y'])**2)

def get_effective_weight(edge, preferences):
    w = edge["weight"]
    if "wheelchair" in preferences and edge.get("has_stairs"): w += 1000
    if "avoid_stairs" in preferences and edge.get("has_stairs"): w += 500
    if "avoid_crowds" in preferences and edge.get("is_crowded"): w += 300
    if "prefer_covered" in preferences and not edge.get("is_covered"): w += 100
    return w

def a_star_search(graph, start, end, preferences):
    start_time = time.perf_counter()
    pq = [(0, 0, start)]
    g_scores = {node: float('inf') for node in graph.adjacency_list}
    g_scores[start] = 0
    previous_nodes = {node: None for node in graph.adjacency_list}
    nodes_explored = 0

    while pq:
        f, current_dist, current_node = heapq.heappop(pq)
        nodes_explored += 1
        
        if current_node == end: break

        for edge in graph.adjacency_list[current_node]:
            neighbor = edge["node"]
            weight = get_effective_weight(edge, preferences)
            tentative_g_score = current_dist + weight

            if tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                previous_nodes[neighbor] = current_node
                
                h = heuristic(graph.node_data[neighbor], graph.node_data[end])
                f_score = tentative_g_score + h
                heapq.heappush(pq, (f_score, tentative_g_score, neighbor))

    path, curr = [], end
    while curr is not None:
        path.append(curr)
        curr = previous_nodes.get(curr)
    path.reverse()
    
    exec_time = (time.perf_counter() - start_time) * 1000
    if not path or path[0] != start: return None, float('inf'), nodes_explored, exec_time
    return path, g_scores[end], nodes_explored, exec_time