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

# A Survey on Spatio-Temporal Graph Neural Networks for Traffic Forecasting
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10411651

- For road traffic prediction but can take some things from it
- They bring up Hyper Graphs (Edges connect more than two nodes) - Could be something to look into
- Mention about difficulties combining the spatio and the temporal part of the GNN
- Also mention about using a bottleneck structure for GNNs: input shape -> 100 -> 25 -> 100 -> output shape to reduce the number of parameters - never seen that always thought you want to go up in dimensions towards the middle but need to test it
- Table 1 gives a good outline of different spatio and temporal architectures