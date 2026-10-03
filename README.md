# Alard Connect: Intelligent Campus Navigation System

**Alard Connect** is a full-stack, graph-based campus mobility and navigation platform built specifically for the Alard Knowledge Park in Marunji. Designed to solve real-world logistical and accessibility challenges within a large university campus, this application combines advanced Data Structures and Algorithms (DSA) with a responsive, interactive user interface. 

At its core, Alard Connect models the university campus as a weighted mathematical graph. It processes spatial coordinates, physical walking distances, and dynamic environmental factors to generate highly optimized routes for students, staff, and visitors. Going beyond standard shortest-path calculations, the system introduces a "Smart Weights" engine that penalizes routes based on user-defined accessibility constraints, ensuring that everyone can navigate the campus safely and efficiently.

## 🌟 Key Features

*   **Algorithmic Route Optimization:** Compares execution time, distance, and nodes explored across multiple algorithms (A*, Dijkstra, BFS) in real-time.
*   **Smart Accessibility Routing:** Dynamically adjusts pathfinding edge weights based on user preferences. Users can toggle options like **Wheelchair Accessible**, **Avoid Stairs**, **Avoid Crowds**, and **Prefer Covered Paths** to force the algorithm to calculate customized, constraint-aware routes.
*   **Alternative Path Generation:** Instead of just a single route, the system utilizes a recursive Depth-First Search (DFS) to calculate and present the top 3 alternative paths, allowing users to pivot if their primary route is blocked.
*   **Event-Driven Navigation:** An integrated campus event dashboard allows users to see upcoming academic and cultural events and instantly generate a route from their current location directly to the event venue with a single click.
*   **Interactive Spatial Mapping:** Features a dynamic, clickable map powered by Vis.js that animates the calculated path step-by-step and provides architectural details about selected buildings.
*   **Dynamic Roadblocks (Admin Mode):** Simulates real-world construction or blockages by allowing administrators to sever edges in the graph in real-time, forcing the system to instantly reroute around the obstacle.

## 🧠 Algorithmic Architecture

The backend routing engine is built on robust graph theory implementation, utilizing several core algorithms depending on the requested operation:

*   **A* Search (Optimal & Fast):** Uses the equation $f(n) = g(n) + h(n)$ to find the shortest path efficiently. The heuristic $h(n)$ is calculated using the Euclidean distance between the spatial $(x, y)$ coordinates of the current node and the destination node, significantly reducing the number of nodes explored compared to standard Dijkstra.
*   **Dijkstra's Algorithm:** Calculates the absolute shortest path by strictly evaluating the accumulated edge weights (walking distance + accessibility penalties) without spatial heuristics.
*   **Breadth-First Search (BFS):** Utilized to find the path with the fewest physical stops (edges) rather than the shortest physical distance. 
*   **Recursive Depth-First Search (DFS):** Powers the "Alternative Routes" feature by exhaustively exploring acyclic paths between the source and destination, sorting them by total weight, and returning the top $k$ optimal alternatives.
*   **Floyd-Warshall:** Maintains an all-pairs shortest path matrix for rapid distance lookups across the entire campus network.

## 🛠️ Technology Stack

*   **Backend:** Python 3, Flask (RESTful API architecture)
*   **Frontend:** HTML5, CSS3 (Custom responsive grid layout), Vanilla JavaScript
*   **Data Serialization:** JSON (Graph adjacency list, node coordinates, event metadata)
*   **Visualization:** Vis.js Network Library

## 🚀 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Alard-connect.git](https://github.com/YOUR_USERNAME/Alard-connect.git)
   cd alard-connect
