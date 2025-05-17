# State-Augmented Opportunistic Routing in Wireless Communication Systems with Graph Neural Networks
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10888417

Take Aways:
- Used RL but seems like random data (both the network topology and packet destination)
- Only uses a 3 layer GCN (No GAT or DGNN)
- Does not use spatio temporal GNN
- I think this is a good starting point to go from

# Hyper-SAGNN: a self-attention based graph neural network for hypergraphs
https://arxiv.org/pdf/1911.02613

- Do primarily hyper-link prediction (other tasks too)
- From a list of vertices (v_1, ..., v_n) that make up a hyper edge they determine if it is part of the graph
- To do this they embedd each vertice twice, one static, one dynamic
- Static uses an encoder -> feed forward network for each vertice and dynamic uses similar structure to GAT
- Then take the distance between the static and dynamic vectors of each vertex (s-d)^2 -> take the mean -> use that vector for prediction
  - This helps determine how much outside influence affects the hyper edge
- Outperforms things like node2Vec, random walk, etc.
- Not sure how much application it is towards SDNs (if it can be represented as a hyper graph) but good to keep in the back of my mind

# RouteNet: Network Modeling and Optimization in SDN
ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9109574

- Uses a GNN to predict key features of a configuration: Delay, Jitter, and Packet Loss (KPIs) distributions
    - Use that prediction as feed back to optimize the current topology (See Figure 1)
- The goal of the GNN is to find the link and path states - represented as hidden states in the GNN used for the final prediction
    - The two depend on each other/circular dependency (Equations 1 and 2)
- Their model is pretty small (32 hidden size for the RNN) - Shows a big improvement over regular queueing theory
- Section 6 Use Cases has some good stuff
    - Create a bunch of candidate network configurations and test them with RouteNet to see which is the best
    - Also contains the data sets they use - NSF, Gean2, and Germany50

# RouteNet-Fermi: Network Modeling with Graph Neural Networks
arxiv.org/abs/2212.12070

- When they use a RNN they don't go by time they go by the path the packet takes
    Ex: Packet travels: L1->L2->L3: The RNN uses L1->L2->L3 embeddings.
- This they use in the final RouteNet-Fermi shown in Fig. 6 RNN is not by time but follows the path of the packets: flow -> queue -> links -> flow -> ...
    - This makes it weaker (they claim it still works though) for non-markovian traffic models since they don't take time as an aspect (not spatio-temporal)
- Initial results with a regular MPNN GNN show they are about the same as a RNN
- OMNet++ for dataset generator
- Table IV has good simulation variables to change
- Scales well to large networks (attribute of GNNs in general) but error still increases a little when increasing network size
- Use RouteNet-Fermi on actual live data gets an even lower error rate

# Research on the Application of Deep Reinforcement Learning in SDN Routing Optimization
https://link.springer.com/chapter/10.1007/978-981-96-4963-1_21

- Uses deep Q network reinforcement learning to optimize routing strategies
  - Does not elaborate on specifics though
- Use randomly generated data on a topology
- Figure 3 shows a comparison between OSPF and Least Load Routing Algorithms

# A Performance Prediction Method Based on Multi-task Spatio-Temporal Convolution Network for SDN Heterogeneous Network
https://link.springer.com/chapter/10.1007/978-981-96-0313-8_20#Abs1

- Uses a STGNN to predict future link performance
- Uses a single topology for testing - STGNN outperforms LSTM and Bi-LSTM by a large margin (by ~35%)
- Good starting point
- Downsides/Places to Improve:
  - Does not test against a lot of baselines (like base GNN)
  - Does not use up to date STGNN for both the spatio (GCN) and temporal (gated convolution) components
  - Only uses one topology


# Building a Digital Twin for network optimization using Graph Neural Networks
https://www.sciencedirect.com/science/article/pii/S1389128622003681
- Dataset: Internet Topology Zoo


https://www.mdpi.com/1999-5903/15/12/377


# Routenet + Spatio Temporal
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10311550


TODO:
Should look into using queing theory for network modeling (that they did in the past)