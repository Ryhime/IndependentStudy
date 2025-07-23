# A Deep Reinforcement Learning Perspective on Internet Congestion Control
- Uses RL to control the congestion control of a sender
- Uses temporal data of the previous latency, throughput, and loss so can be decentralized
- Achieves better results than CUBIC and can adapt quickly to changing network enviornments
- Show Reward Function and Figure 7
- THINGS TO ADD: Since I am doing an SDN I have global view of the network so add Jaine's fairness metric and QoS
  - QoS could be used as the danger zones that were talked about in the past


# Targeted Congestion Control With Deep RL
- Modifies last mentioned paper with a latency target in its reward function
- About the same throughput as BBR, CUBIC, and last paper
  - But has lower latency since latency target is in the reward function
- NOTE: A good example of adding extra terms to the reward function to see results

# Deep RL + Probe Bandwidth
- Combines deep RL in congestion control with BBR
- RL agent picks 1x, 1.25x, and divide by 1.25
- While RL agent is running, probing the available bandwidth
- If bandwidth is not fully utilized and RL agent decides to increase an extra 1.25x increase is added to cwnd
- Fills the available bandwidth really quickly since the extra 1.25x is added


# A CC Algorithm for Enhanced QoE in Real Time Networks
- Similar to previous papers
- Uses a LSTM to predict available bandwidth from past network metrics
- Uses the output of the LSTM prediction and past network states to adjust CWND using actor critic RL agent
- Higher throughput, less loss, and lower RTT especially on lossy networks