def floyd_warshall(graph):
    nodes = list(graph.adjacency_list.keys())
    dist = {u: {v: float('inf') for v in nodes} for u in nodes}
    
    for u in nodes:
        dist[u][u] = 0
        for edge in graph.adjacency_list[u]:
            dist[u][edge["node"]] = edge["weight"]

    for k in nodes:
        for i in nodes:
            for j in nodes:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                
    return dist