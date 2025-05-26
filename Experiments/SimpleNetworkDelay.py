import networkx as nx
import random
import simpy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def send_packet(env, graph, src, dest, delays, graphs):
    path = nx.shortest_path(graph, source=src, target=dest)
    print(len(path))
    total_queueing = 0

    for n in path:
        node = graph.nodes[n]
        resource = node["queueSizes"]

        # Request access to the link (queueing delay happens here)
        request_time = env.now
        node["inQueue"] += 1
        node["inQueueHistory"].append(node["inQueue"])
        with resource.request() as req:
            yield req
            queueing_delay = env.now - request_time
            total_queueing += queueing_delay

            yield env.timeout(node["linkDelay"])
            node["inQueue"] -= 1
            node["inQueueHistory"].append(node["inQueue"])
            total_queueing += node["linkDelay"]

    delays.append(total_queueing)
    graphs.append(nx.Graph(graph))


def run_simulation(num_packets=100, link_delay = 10, queue_size = 2):
    env = simpy.Environment()
    topology_file = "/home/ryhime/Desktop/gnnet-ch21-dataset-test/ch21-test-setting-1/50/graphs/graph-50-0-1.txt"
    G = nx.read_gml(topology_file, destringizer=int)
    for n in G.nodes:
        G.nodes[n]["queueSizes"] = simpy.Resource(env, capacity=queue_size)
        G.nodes[n]["inQueue"] = 0
        G.nodes[n]["linkDelay"] = link_delay
        G.nodes[n]["inQueueHistory"] = []

    delays = []
    graphs = []

    def packet_generator():
        for i in range(num_packets):
            env.process(send_packet(env, G, random.randint(0, 20), random.randint(20, 41), delays, graphs))
            if (i % 1000 == 0):
                yield env.timeout(100000)
            yield env.timeout(np.random.uniform(50, 250))

    env.process(packet_generator())
    env.run()

    # Return the average delay over time
    averages = []
    print(delays)
    n = 100
    for i, d in enumerate(delays):
        if (i < n): continue
        sm = sum(delays[i-n:i+1])
        averages.append(sm/float(n))

    return (averages, graphs)


if __name__ == "__main__":
    delays, graphs = run_simulation(10000)
    # Smooths the series by getting the mean
    # NOTE: IDK if should take this out or have it be part of the model?
    series = pd.Series(delays)
    # delays = series.rolling(window=5).mean()

    plt.plot(range(len(delays)), delays)
    plt.title("Average End to End Delay Over Time For Last 100 Packets")
    plt.xlabel("Packet #")
    plt.ylabel("Average End to End Delay")
    plt.grid(True)
    plt.savefig("Delays.png")