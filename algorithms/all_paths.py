def get_effective_weight(edge, preferences):
    w = edge["weight"]
    if "wheelchair" in preferences and edge.get("has_stairs"): w += 1000
    if "avoid_stairs" in preferences and edge.get("has_stairs"): w += 500
    if "avoid_crowds" in preferences and edge.get("is_crowded"): w += 300
    if "prefer_covered" in preferences and not edge.get("is_covered"): w += 100
    return w

def get_top_k_paths(graph, start, end, preferences, k=3):
    def dfs(current, destination, visited, path, current_dist):
        if current == destination:
            paths.append((list(path), current_dist))
            return
            
        for edge in graph.adjacency_list.get(current, []):
            neighbor = edge["node"]
            weight = get_effective_weight(edge, preferences)
            
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, destination, visited, path, current_dist + weight)
                path.pop()
                visited.remove(neighbor)

    paths = []
    if start in graph.adjacency_list and end in graph.adjacency_list:
        dfs(start, end, set([start]), [start], 0)
        
    paths.sort(key=lambda x: x[1])
    return paths[:k]