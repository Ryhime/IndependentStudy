import networkx as nx
import matplotlib.pyplot as plt
import random

# --- 1. Build the network ---
G = nx.DiGraph()
# Define edges with capacities (packets per time slot)
edges = [
    ("src1", "bottleneck", 2),
    ("src2", "bottleneck", 2),
    ("bottleneck", "dst", 2)
]
for u, v, cap in edges:
    G.add_edge(u, v, capacity=cap)

# --- 2. Define flows with paths ---
flows = {
    "f1": nx.shortest_path(G, "src1", "dst"),
    "f2": nx.shortest_path(G, "src2", "dst")
}

# Initialize CWND and history
cwnd = {f: 1 for f in flows}       # start at 1 packet
ssthresh = {f: 8 for f in flows}  # arbitrary slow-start threshold
history = {f: [] for f in flows}

# AIMD parameters
AI = 1     # additive increase per RTT
MD = 0.5   # multiplicative decrease factor

SLOTS = 200

# --- 3. Simulation Loop ---
for t in range(SLOTS):
    # Count load on each edge
    edge_load = {e: 0 for e in G.edges}
    # Tentatively send cwnd packets per flow
    for f, path in flows.items():
        for u, v in zip(path, path[1:]):
            edge_load[(u, v)] += cwnd[f]

    # Apply capacity checks and update CWNDs
    flows_lost = set()
    for (u, v), load in edge_load.items():
        cap = G[u][v]['capacity']
        if load > cap:
            # packet loss occurred on this link
            for f, path in flows.items():
                if (u, v) in zip(path, path[1:]):
                    flows_lost.add(f)

    # Update cwnd based on losses
    for f in flows:
        if f in flows_lost:
            ssthresh[f] = max(cwnd[f] * MD, 1)
            cwnd[f] = max(cwnd[f] * MD, 1)
        else:
            # additive increase
            cwnd[f] += AI

        history[f].append(cwnd[f])

# --- 4. Plot the results ---
for f, data in history.items():
    plt.plot(data, label=f)
plt.xlabel("Time slot")
plt.ylabel("CWND")
plt.title("TCP AIMD congestion window over time")
plt.legend()
plt.grid(True)
plt.savefig("Out.png")