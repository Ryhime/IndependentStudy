# Datasets
## Internet Topology Zoo
https://bnn.upc.edu/challenge/gnnet2021/dataset/
Has a leader board from 2023 for a good reference


## Standford Collection of Graph Datasets
Includes networks:
https://snap.stanford.edu/data/


https://networkrepository.com/temporal-networks.php



# Use Cases
## Dynamic Routing Algorithm Using STGNN
1 - Get topology from the Internet Topology Zoo (Plenty of graphs to work with)
2 - Run packets simulation through the topology
3 - Run a STGNN to try to predict things like jitter, average delay, delay per node
4 - Use that feed back as a reinforcement loss for routing configuration

Some metrics - queue length, 