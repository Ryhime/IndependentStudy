# Focus Papers Off of NeuRoute

## Traffic-aware Routing with Software-defined Networks Using Reinforcement Learning and Fuzzy Logic
- Takes into account lossy links
- Use bandwidth, delay, and loss as the parameters for the links
- Reward is given if any of the above values exceed a threshold (Go above QoS requirements)
- Replaces the link cost and runs Dijkstra's (Can I use A* here?) (Is this a bad feature??)
- Do video streaming on different traffic intensities (5 Mbps -> 15 Mbps)
- Shows that it significantly out performs OSPF and slightly outperforms another dynamic routing scheme that uses RL


## Including Artificial Intelligence in a Routing Protocol Using Software Defined Networks
- Splits its virtual network into sub nets one subnet only sends packets to the other subnets
- Nothing really good here expect that they initialize all the edge weights with OSPF

## Experience-driven Networking: A Deep Reinforcement Learning based Approach
- In the reward function use a variable alpha to set how important delay and throughput is to the reward
- Put together k active communication sessions between users, the RL is determined by how well each communication session is
- I REALLY LIKE THE ABOVE - THIS CAN BE MODIFIED SO EACH COMMUNICATION SESSION IS SOMETHING DIFFERENT - WEIGHTS CAN BE APPLIED TO DETERMINE WHICH SESSIONS ARE THE MOST IMPORTANT
- Look into Deep RL and actor + critic based RL
- Use a feed forward network for both actor and critic networks
- Performance Metrics: e2e throughput, e2e packet delay, and network total utility
- Shows a large performance increase in all three of the above
- Has a lot of RL stuff that I need to catch up on - something to read over next weeks papers
- Areas to improve: Only uses a feed forward network, only goes up to 40 Mbps, and does not simulate other types of users

## SmartCC: A Reinforcement Learning Approach for Multipath TCP Congestion Control in Heterogeneous Networks
- Point out a problem with MPTCP is using multiple paths like WiFi and LTE if one is stronger than the offer the out of order buffer fills quick on the recieving device
- Look into TCP ramp up: If a packet is lost the cwnd is cut in half if an ACK is got it increases cwnd by 1 where cwnd is how many packets are sent at once
- Use RL to determine TCP ramp up by using how fast ACK packets come in as the reward function - WORTH LOOKING INTO FOR MY IMPLEMENTATION
- Done async on a different device RL training so does not impact performance of actual network transmission time
- Mention that they do not account for fairness among different links so one could starve out
- The learned TCP cwnd window changes outperformed other methods but could not be explained (could they be explained now a days since research has been put into that??)

## Dynamic TCP Initial Windows and Congestion Control Schemes Through Reinforcement Learning
- Observes that a lot of connections are closed during TCP ramp up so it never reaches max capacity
- Small flows heavily rely on initial window while larger ones rely on the congestion control algorithm overtime
- Group everyone on a subnet to the same group -> RL tries to find the best initial window for that group on session start
- For the initial window size uses past rewards as input into a LSTM
- The reward function is calculated by comparing the current RTT with RTT_{min} and throughput with throughput_{max}
- Each subnet has a list of rewards given at different times each reward represents the network condition so you have time series data
- Can "combine" subnets if the subnets share the same properties and are in the same ISP, Province, going up the chain

- Congestion Control RL
  - Uses Throughput, RTT, and Loss Rate as state input to the NN
  - Use an actor and critic RL scheme
  - Also shows performance gain

NOTE: Could I include traffic classification to help with the window ramp up?



## Survey
A Survey of Machine Learning Techniques Applied
to Software Defined Networking (SDN):
Research Issues and Challenges


Modeling TCP Performance using Graph Neural Networks