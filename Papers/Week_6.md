# Book Takeaways
- Dropping a packet if queue size gets too large (RED)
  - To signal to the host congestion is occuring
- Flow Admission
- Marking Packets with ECN tag to show that a router is being backed up


# Performance Analysis of BBR Congestion Control Protocol Based on NS3
- Comapre different congestion control algorithms with Google's BBR
- BBR uses the estimated bandwidth and RTT - Equation 1
- Find that BBR is good at link utilization but is not fair straining out hosts that use different congestion algorithms
- BBR does not take into account duplicate ACKs when deciding CWND so it could push packets on a fast but unreliable link causing lots of packet loss
- BBR struggles with larger queue sizes with other congestion algorithms
  - A full queue -> longer RTT -> BBR chooses to send more packets since the RTT increases
  - Other TCP algorithms are off of loss and timeout so for a larger queue size they ramp up quick filling up the queue so BBR starves out
  - Once queues fill up they start dropping packets making the other congestion control algorithms slow down allowing BBR to pick up more CWND
- Takes less resources when the RTT is low since it uses RTT in the CWND equation comapred to other congestion control algorithms

# Introduction to BBRv2 Congestion Control
- Make a point that classic TCP congestion algorithms don't preemptively prevent congestion only take effect when congestion happens - want to prevent congestion before it happens
- Re points out problems
  - RTT unfairness
  - Unresponsive to Packet Loss
  - Fairness on different queue sizes
- V2 still does not fix the RTT unfairness but fixes not accounting for lost packets
- Fixes packet loss though
  - Detects packet loss by seeing how many ACKs were received out of the sent packets
  - Also supports ECN tagging by the routers if queue lengths get too long decreasing the CWND if a majority of packets are marked with the ECN tag
    - Works since Google is using this within their data centers so they have access to all their routers but harder to implement on a decentralized network

# Enhanced BBR Congestion Control Algorithm for Improving RTT Fairness
- RTT increases when the queues fill up - So BBR starts to send more packets when queues fill up which you don't want
- Fixes the RTT unfairness of BBR by introducing an extra step that slows down the CWND gain if it detects queues are filling up
  - This limits the CWND gain from the RTT portion
- Compared with the original BBR much more fair when two flows have 10 ms and 100 ms RTT
- Check Algorithm Two for more info


# A QoS-Based Fairness-Aware BBR Congestion Control Algorithm Using QUIC
- Combine BBR with things from classic TCP congestion algorithms
  - Packet loss divide the CWND by 2
  - If queue length gets too full start changing the CWND towards the last CWND used
    - Does not specify how they detect when a queue size gets to a certain length
- Outperforms BBR throughput
- Also decreases the loss by a large margin (Show that graph - Fig 5b)
- Shows sawtooth pattern of other TCP congestion algorithms - BBR is more random showing it does not find the max then back off
