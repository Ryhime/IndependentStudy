# Graph-based deep learning for communication networks: A survey
https://www.sciencedirect.com/science/article/abs/pii/S0140366421004874

Take Aways:
- Overview of a lot of different wire and wireless applications

# An Overview of the Application of Graph Neural Networks in Wireless Networks
https://arxiv.org/pdf/2107.03029

Take Aways:
- Main problems in wireless is resource allocation and link scheduling
- Link scheduling could be a good approach for wired SDNs
- Spatio-temporal GNNs are need for dynamic graphs - (The temporal part can either be RNN, LSTM, Bi-LSTM, or Transformer based)


# Spatio-Temporal Graph Neural Networks: A Survey
https://arxiv.org/pdf/2301.10569

Take Aways:
- Mention graph transformer as a big go to
- Has a spatio component - GCN, GAT, etc.
- Has a temporal component - 1D-CNN, Attention LSTM, Bi-LSTM, Transformer, etc.
- Augmented graph data like using a gaussian smooth on images

# State-Augmented Opportunistic Routing in Wireless Communication Systems with Graph Neural Networks
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10888417

Take Aways:
- Used RL but seems like random data (both the network topology and packet destination)
- Only uses a 3 layer GCN (No GAT or DGNN)
- Does not use spatio temporal GNN
- I think this is a good starting point to go from

# A Survey on Spatio-Temporal Graph Neural Networks for Traffic Forecasting
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10411651

- For road traffic prediction but can take some things from it
- They bring up Hyper Graphs (Edges connect more than two nodes) - Could be something to look into
- Mention about difficulties combining the spatio and the temporal part of the GNN
- Also mention about using a bottleneck structure for GNNs: input shape -> 100 -> 25 -> 100 -> output shape to reduce the number of parameters - never seen that always thought you want to go up in dimensions towards the middle but need to test it
- Table 1 gives a good outline of different spatio and temporal architectures

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

# RouteNet: Network Modeling and Optimization in SDN



TODO:
- Continue looking at spatio-temporal GNNs
