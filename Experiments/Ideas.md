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


# Things to consider:
- Would need to train the STGNN predicting jitter, average delay, delay per node before hand since it is predicting at the next time point
- How would I then change the routing configuration? Would it be a transformer GNN?
- Time complexity of the system
- Test training the STGNN on a different topology and applying it to a different one as well as applying it to the same it was trained on


Some metrics - queue length, average delay, delay per node
Compare it with things like a DNN, LSTM


# Simulation Ideas
- Can get fancy like having some users have heavy loads all at once, some downloading files, etc.
- Can also have QoS requirements which I think are already in Internet Topology Zoo
- To get the average network metrics can use ARMA (Can also use ARMA-Conv for predictions then)
- ARMA CONV IS PERFECT FOR THIS SCENARIO ALSO TRY WITH DIFFERENT GNNS THOUGH


# For the dynamic routing part have backup routes initially can use:
- Reinforcement
- Least Load
- The multiple paths found first can be weighted with the length to each destination node