# Focus - Dynamic Routing

## Network Recovery Optimization in SDN
https://www.fruct.org/files/publications/volume-37/fruct37/Pap.pdf
- Lays out different ways to combat things like a link/router going down in a topology
- Everything is centralized so if something goes down the SDN controller is called instead of a decentralized Dikjstra's
- Creates a bottleneck for the SDN controller
- SDN controller can hold multiple backup paths which doesn't overload the individual routers/switches
- When a link goes down by the time a new routing algorithm converges about 50% of packets are lost in that timespan without a backup path
- "this approach envisions leveraging neural networks to anticipate potential failures based on historical and real-time telemetry data. The goal is to shift from a purely reactive paradigm toward a predictive and preemptive one."
- Is there a way to predict link failures????????????????

## Comprehensive Analysis of Dynamic Routing Protocols in Computer Networks
- Lays out different routing algorithms (both dynamic and static) - only looking at interior protocols
- The most interesting one is Enchance Interior Gateway Routing Protocol
  - It sets a weight for each edge by bandwidth, delay, reliability, load, and MTU
  - Then computes a loop free routing scheme with Diffusing Update Algorithm
- OSPF also sets weights to edges then uses Dijkstra's to compute routing scheme

## NeuRoute: Predictive Dynamic Routing for Software-Defined Networks (Want to continue reading citations off of this paper)
- Optimizes due to Maxiumum throughput minimum cost dynamic routing using the predicted traffic matrix
  - They formulate it as a linear program and show that it is NP-Complete (Perfect for ML) (Can look into this later for funsies)
- Say that changing a links cost + recomputing paths is as expensive as a link going down (check with professor if that is true)
- They use an estimator since measuring the current traffic matrix would take too long to send up to the SDN controller
- In the context of a GNN each edge can be a vector in the network traffic
- Use an LSTM for traffic matrix prediction and a DNN for predicting the routing routes (they predict the routes directly)
- They claim this shows the same performance as other dynamic routing while being quicker
- A GNN IS QUICKER THAN A LSTM
- Use an already known dynamic routing protocol to create training data
- "the trained model executes and finds the near optimal path in 30 ms compared to the regular execution time of 120ms" - since this is at prediction time
- I WANT TO IMPLEMENT THIS
- Can I also do multi shot (t+1) and (t+2) if the accuracy is that high
- If you give probabilities could that also be a way around link failures?

## OSPF Routing Protocol Performance in Software Defined Networks
- Nothing useful - they literally just said OSPF works on physical + virtually simulated topologies

## NeuTM: A Neural Network-based Framework for Traffic Matrix Prediction in SDN
- Mentions ARMA was used in the past so ARMAConv may be a good use (also covers non-linear functions through activation functions)
- This boils down to a time series prediction
- Points out that FFNNs cannot capture time -> LSTMs cannot capture structure but ST-GNNs capture structure and time
- They flatten the traffic matrix to a vector so they completely lose network structure
- Look into GEANT data set

# Deep Reinforcement Learning Based QoS-Aware Routing in Knowledge-Defined Networking
- Use a traffic matrix for input into the reinforcement learning neural network
- Uses a CNN (does not capture time because of this though)
- Does much better than a DNN

file:///home/ryhime/Downloads/7126-21793-1-PB.pdf