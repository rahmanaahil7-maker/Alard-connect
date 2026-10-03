from flask import Flask, request, jsonify, send_from_directory
import json
from algorithms.graph import CampusGraph
from algorithms.dijkstra import dijkstra_shortest_path
from algorithms.bfs import bfs_fewest_edges_path
from algorithms.a_star import a_star_search
from algorithms.all_paths import get_top_k_paths

app = Flask(__name__, static_folder='static')
campus = CampusGraph()
campus.load_from_json('data/campus.json')

@app.route('/')
def index(): 
    return send_from_directory('templates', 'index.html')

@app.route('/<path:filename>')
def serve_html(filename):
    if filename.endswith('.html'): return send_from_directory('templates', filename)
    return send_from_directory('static', filename)

@app.route('/api/route', methods=['POST'])
def get_route():
    data = request.json
    src, dest = data['source'], data['destination']
    algo_choice = data.get('algorithm', 'a_star')
    preferences = data.get('preferences', [])
    
    d_path, d_dist, d_exp, d_time = dijkstra_shortest_path(campus, src, dest, preferences)
    b_path, b_dist, b_exp, b_time = bfs_fewest_edges_path(campus, src, dest, preferences)
    a_path, a_dist, a_exp, a_time = a_star_search(campus, src, dest, preferences)
    
    top_paths = get_top_k_paths(campus, src, dest, preferences, k=3)
    routes_payload = []
    
    for idx, (p, d) in enumerate(top_paths):
        # Calculate base physical distance (without preference penalties) for display
        physical_dist = 0
        for i in range(len(p)-1):
            for e in campus.adjacency_list[p[i]]:
                if e["node"] == p[i+1]:
                    physical_dist += e["weight"]
                    break
                    
        routes_payload.append({
            "id": idx + 1,
            "path": p,
            "distance": physical_dist, 
            "time": round(physical_dist / 80) if physical_dist != float('inf') else 0
        })

    return jsonify({
        "routes": routes_payload,
        "comparison": {
            "dijkstra": {"dist": d_dist, "nodes": d_exp, "time": f"{d_time:.4f} ms"},
            "bfs": {"dist": b_dist, "nodes": b_exp, "time": f"{b_time:.4f} ms"},
            "astar": {"dist": a_dist, "nodes": a_exp, "time": f"{a_time:.4f} ms"}
        }
    })

@app.route('/api/block', methods=['POST'])
def block_road():
    data = request.json
    campus.block_road(data['u'], data['v'])
    return jsonify({"status": "Success"})

@app.route('/api/events', methods=['GET'])
def get_events():
    with open('data/events.json') as f: return jsonify(json.load(f))

@app.route('/api/graph', methods=['GET'])
def get_graph():
    with open('data/campus.json') as f: return jsonify(json.load(f))

if __name__ == '__main__':
    print("🚀 API Running on http://127.0.0.1:5000")
    app.run(debug=True)