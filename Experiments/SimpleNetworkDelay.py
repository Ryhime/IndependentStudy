import networkx as nx
import random
import simpy
import matplotlib.pyplot as plt
import pandas as pd

link_delay = 50
c = 5

env = simpy.Environment()
topology_file = "/home/ryhime/Desktop/gnnet-ch21-dataset-test/ch21-test-setting-1/50/graphs/graph-50-0-1.txt"
G = nx.read_gml(topology_file, destringizer=int)
for n in G.nodes:
    G.nodes[n]["queueSizes"] = simpy.Resource(env, capacity=c)

def send_packet(env, graph, src, dest, delays):
    path = nx.shortest_path(graph, source=src, target=dest)
    total_queueing = 0

    for n in path:
        resource = graph.nodes[n]["queueSizes"]

        # Request access to the link (queueing delay happens here)
        request_time = env.now
        with resource.request() as req:
            yield req
            queueing_delay = env.now - request_time
            total_queueing += queueing_delay

            yield env.timeout(link_delay)
            total_queueing += link_delay

    delays.append(total_queueing)


def run_simulation(num_packets=100):
    results = []

    def packet_generator():
        for _ in range(num_packets):
            env.process(send_packet(env, G, random.randint(0, 20), random.randint(21, 40), results))
            interarrival = random.expovariate(1/3.0)
            yield env.timeout(interarrival)

    env.process(packet_generator())
    env.run()
    return results

delays = run_simulation()
# Smooths the series by getting the mean
# NOTE: IDK if should take this out or have it be part of the model?
series = pd.Series(delays)
delays = series.rolling(window=20).mean()

plt.scatter(range(len(delays)), delays)
plt.title("Line Graph with Custom X")
plt.xlabel("Time (s)")
plt.ylabel("Measurement")
plt.grid(True)
plt.savefig("Delays.png")