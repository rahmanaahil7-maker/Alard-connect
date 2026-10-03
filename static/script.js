async function loadLocations() {
    if (document.getElementById("campus-locations")) {
        try {
            const res = await fetch('/api/graph');
            const data = await res.json();
            const datalist = document.getElementById("campus-locations");
            datalist.innerHTML = "";
            Object.keys(data.nodes).forEach(node => { datalist.innerHTML += `<option value="${node}">`; });
        } catch (e) {
            console.error("Failed to load locations:", e);
        }
    }
}

function calculateRoute() {
    const source = document.getElementById("source").value;
    const dest = document.getElementById("destination").value;
    const algo = document.getElementById("algorithm").value;
    
    const prefs = [];
    if(document.getElementById('pref-wheelchair')?.checked) prefs.push('wheelchair');
    if(document.getElementById('pref-stairs')?.checked) prefs.push('avoid_stairs');
    if(document.getElementById('pref-crowds')?.checked) prefs.push('avoid_crowds');
    if(document.getElementById('pref-covered')?.checked) prefs.push('prefer_covered');
    
    window.location.href = `result.html?src=${encodeURIComponent(source)}&dest=${encodeURIComponent(dest)}&algo=${algo}&prefs=${prefs.join(',')}`;
}

document.addEventListener("DOMContentLoaded", async () => {
    loadLocations();

    if (document.getElementById("path-container")) {
        const urlParams = new URLSearchParams(window.location.search);
        const source = urlParams.get('src') || "Main Gate";
        const dest = urlParams.get('dest') || "Seminar Hall";
        const algo = urlParams.get('algo') || "a_star";
        const prefsStr = urlParams.get('prefs');
        const prefs = prefsStr ? prefsStr.split(',') : [];
        
        document.getElementById("route-summary").innerText = `${source} to ${dest}`;

        try {
            const response = await fetch('/api/route', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source: source, destination: dest, algorithm: algo, preferences: prefs })
            });
            
            if (!response.ok) throw new Error(`Server returned status ${response.status}.`);

            const resData = await response.json();
            const routes = resData.routes;
            const container = document.getElementById("path-container");
            const tabsContainer = document.getElementById("route-tabs");
            
            document.getElementById("cmp-a-dist").innerText = resData.comparison.astar.dist;
            document.getElementById("cmp-a-nodes").innerText = resData.comparison.astar.nodes;
            document.getElementById("cmp-a-time").innerText = resData.comparison.astar.time;
            document.getElementById("cmp-d-dist").innerText = resData.comparison.dijkstra.dist;
            document.getElementById("cmp-d-nodes").innerText = resData.comparison.dijkstra.nodes;
            document.getElementById("cmp-d-time").innerText = resData.comparison.dijkstra.time;
            document.getElementById("cmp-b-dist").innerText = resData.comparison.bfs.dist;
            document.getElementById("cmp-b-nodes").innerText = resData.comparison.bfs.nodes;
            document.getElementById("cmp-b-time").innerText = resData.comparison.bfs.time;

            if (!routes || routes.length === 0) {
                tabsContainer.innerHTML = "";
                container.innerHTML = "<h3 style='color:red;'>Destination unreachable with current preferences.</h3>";
                return;
            }

            const graphRes = await fetch('/api/graph');
            const graphData = await graphRes.json();
            const nodes = new vis.DataSet(Object.keys(graphData.nodes).map(nodeKey => ({
                id: nodeKey, label: nodeKey, x: graphData.nodes[nodeKey].x, y: graphData.nodes[nodeKey].y, info: graphData.nodes[nodeKey].info,
                color: { background: '#cbd5e1', border: '#94a3b8' }, font: { color: '#1e293b' }, shape: 'box'
            })));
            
            const edges = new vis.DataSet(graphData.edges.map(e => ({
                id: `${e.source}-${e.target}`, from: e.source, to: e.target, 
                label: `${e.weight}m`, color: { color: '#e2e8f0' }, width: 2
            })));

            const network = new vis.Network(document.getElementById('campus-map'), {nodes, edges}, {physics: false, interaction: { hover: true }});
            
            let currentAnimInterval = null;

            window.renderRoute = function(routeIndex) {
                const data = routes[routeIndex];
                document.querySelectorAll('.route-tab').forEach((tab, i) => {
                    if (i === routeIndex) tab.classList.add('active');
                    else tab.classList.remove('active');
                });

                document.getElementById("total-distance").innerText = `${data.distance} m`;
                document.getElementById("walking-time").innerText = `~${data.time} mins`;

                container.innerHTML = "";
                data.path.forEach((node, index) => {
                    const stepDiv = document.createElement("div");
                    stepDiv.className = "route-step";
                    let iconClass = index === 0 ? "fa-play" : (index === data.path.length - 1 ? "fa-flag-checkered" : "fa-location-dot");
                    stepDiv.innerHTML = `<div class="step-icon"><i class="fa-solid ${iconClass}"></i></div>
                        <div><h4 style="margin: 0; color: #1e293b;">${node}</h4><span style="font-size: 0.8rem; color: #64748b;">${index < data.path.length - 1 ? 'Proceed next' : 'Destination'}</span></div>`;
                    container.appendChild(stepDiv);
                });

                nodes.forEach(n => nodes.update({id: n.id, color: { background: '#cbd5e1', border: '#94a3b8'}, font: {color: '#1e293b', bold: false}}));
                edges.forEach(e => edges.update({id: e.id, color: { color: '#e2e8f0'}, width: 2}));

                if (currentAnimInterval) clearInterval(currentAnimInterval);
                if (data.path.length > 0) {
                    let step = 0;
                    currentAnimInterval = setInterval(() => {
                        const currentNode = data.path[step];
                        nodes.update({id: currentNode, color: { background: '#4f46e5', border: '#3730a3'}, font: {color: '#ffffff', bold: true}});
                        if (step > 0) {
                            const prevNode = data.path[step-1];
                            const edgeId1 = `${prevNode}-${currentNode}`;
                            const edgeId2 = `${currentNode}-${prevNode}`;
                            if (edges.get(edgeId1)) edges.update({id: edgeId1, color: { color: '#4f46e5'}, width: 4});
                            if (edges.get(edgeId2)) edges.update({id: edgeId2, color: { color: '#4f46e5'}, width: 4});
                        }
                        step++;
                        if (step >= data.path.length) clearInterval(currentAnimInterval);
                    }, 500);
                }
            };

            tabsContainer.innerHTML = "";
            routes.forEach((rt, i) => {
                tabsContainer.innerHTML += `
                    <div class="route-tab" onclick="renderRoute(${i})">
                        <h4>Route ${i + 1}</h4>
                        <p>${rt.distance}m • ${rt.time} min</p>
                    </div>`;
            });
            renderRoute(0);

        } catch (error) {
            console.error("Routing Error:", error);
            document.getElementById("path-container").innerHTML = `<div style="padding: 1rem; background: #fee2e2; border: 1px solid #ef4444; border-radius: 8px; color: #b91c1c;"><strong>Backend Error:</strong><br> ${error.message}</div>`;
        }
    }

    if (document.getElementById("events-container")) loadEvents();
});

// Used by the button on the Events page
window.navigateEvent = function(destination) {
    const source = document.getElementById("event-origin").value;
    window.location.href = `result.html?src=${encodeURIComponent(source)}&dest=${encodeURIComponent(destination)}&algo=dijkstra`;
};

async function loadEvents() {
    const res = await fetch('/api/events');
    const data = await res.json();
    const container = document.getElementById("events-container");
    container.innerHTML = "";
    
    data.events.forEach(event => {
        container.innerHTML += `
            <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <p style="color: var(--primary); font-weight: bold; margin-bottom: 0.5rem; font-size: 1.1rem;">${event.time}</p>
                    <h3 style="margin-bottom: 0.5rem;">${event.name}</h3>
                    <p style="color: var(--text-muted); margin-bottom: 1.5rem;"><i class="fa-solid fa-location-dot"></i> ${event.location}</p>
                </div>
                <button class="btn" style="background: var(--surface); color: var(--primary); border: 2px solid var(--primary);" onclick="navigateEvent('${event.location}')">[ Navigate ]</button>
            </div>
        `;
    });
}