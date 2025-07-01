# FTG-Net: Hierarchical Flow-to-Traffic Graph Neural Network for DDoS Attack Detection
- Have two levels of graphs
  - Packet level - Which packets are sent within the window
  - Traffic Graph - Topology of network
- Each node in the traffic graph corresponds to one packet level graph
- The output of the packet level graph is concatenated with the vector in each node of the traffic graph 
  - Then a GNN is run on the traffic level graph to make node level predictions
- The nature of the packet level graph captures packet length and how close they are sent to eachother which helps capture DDOS activity
- About the same results as other methods
  - There is little room for improvement other methods are at 99%+ accuracy and F1

# Building a Graph-based Deep Learning network model from captured traffic traces
- Sets 4 "rules" for modeling a network as a graph
  - Each link and port has a one-to-one
  - The state of ports of the same device will be affected by each other due to dependencies of shared resources (the device embedding should take into account all ports)
  - The state of ports of the same device will be affected by the state of the links and ports they traverse
  - The state of links and ports will depend on the state of flows passing through them
- For the actual modeling they use a RNN for the flow message passing so the graph can make sense of time of the flow
- The one from last week does not do this

# Graph Neural Modeling of Network Flows
- Show how important modeling the edges in the graph is to model performance
- Compare their method (a rename R-GAT to use edge embeddings) to GNNs that do not have the ability to have edge values
  - Has much less loss than GNNs that do not have edge values including GAT and SAGE
- They don't show a comparison to other GNNs that use edge attributes like R-GCN

# A DDoS Attacks Detection Scheme Using Host-Connection Graph Representation and GCN
- Models the graph as a source node -> flow node -> destination node
- Gets 99% accuracy on DDoS attack prediction but does not do a baseline test...
- Don't like this method since it abstracts the flow away a lot and doesn't completely capture the topology