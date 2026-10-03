import json

class CampusGraph:
    def __init__(self):
        self.adjacency_list = {}
        self.node_data = {}

    def load_from_json(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
            
        for node, info in data.get("nodes", {}).items():
            self.add_node(node, info)
            
        for edge in data.get("edges", []):
            self.add_edge(
                edge["source"], edge["target"], edge["weight"],
                has_stairs=edge.get("has_stairs", False),
                is_crowded=edge.get("is_crowded", False),
                is_covered=edge.get("is_covered", False)
            )

    def add_node(self, node, info):
        self.node_data[node] = info
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, u, v, weight=1, directed=False, has_stairs=False, is_crowded=False, is_covered=False):
        edge_data = {"node": v, "weight": weight, "has_stairs": has_stairs, "is_crowded": is_crowded, "is_covered": is_covered}
        self.adjacency_list[u].append(edge_data)
        if not directed:
            reverse_edge = {"node": u, "weight": weight, "has_stairs": has_stairs, "is_crowded": is_crowded, "is_covered": is_covered}
            self.adjacency_list[v].append(reverse_edge)

    def block_road(self, u, v, directed=False):
        if u in self.adjacency_list:
            self.adjacency_list[u] = [edge for edge in self.adjacency_list[u] if edge["node"] != v]
        if not directed and v in self.adjacency_list:
            self.adjacency_list[v] = [edge for edge in self.adjacency_list[v] if edge["node"] != u]