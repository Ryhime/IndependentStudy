# Overcoming Fairness and Latency Challenges in BBR With an Adaptive Delay Detection
- Netflix and Amazon use BBR around 20% of the internet uses BBR
- BBR has a phase ProbeRTT where it drains its queues by sending a lot less packets to measure the current RTT that doesn't include queue delay
  - Only set to a fixed 4 packets during this phase
- BBR-R sets this to alpha * Bottleneck Bandwidth * RTT where alpha < 1
  - This ensures that the probing is always less than the current cwnd since cwnd uses Bottleneck Bandwidth * RTT
- Compared to BBR has a lot shorter of a queueing delay and has a higher Jain's Fairness index (0 to 1)
  - Far far less queuing delay than CUBIC but less fair than CUBIC

# CUBIC: A New TCP-Friendly High-Speed TCP Variant
- Claims original congestion algos like Reno don't scale up the cwnd quick enough for networks with a higher bandwidth and RTT
  - Example used it takes 50,000 RTT's to reach 
- CUBIC comes after BIC-TCP which uses midpoint between last RTT and current RTT to scale the cwnd so scales well and converges
- Uses BIC-TCP as a starting point
  - BIC-TCP starts by doing an additive increase (while the midpoint is larger than S_{max})
  - Then it grows by the midpoint which forms a log like curve
- Cubic grows by a power of 3
  - Adds from the last max window size before the last loss event
  - Adds the time between a counter and the time it took to reach the last loss event
  - So it slows down when the time elaspes around the same time it took for congestion on the last congestion event
- More fair than BIC-TCP and gets round the same link utilization
- In general moves faster to the estimated BDP since it uses a cubic function

# Performance Comparison Between TCP Reno and TCP Vegas
- Compares Reno and Vegas
  - Reno - Loss based aggressive until sees loss - goal is to fill up the queues as fast as possible
  - Vegas - RTT based changes CWND by the expected compared to the actual RTT - Does well in enviornments with short queueing delay
- In environments with only other Reno and only other Vegas congestion algos Vegas does better
- In environments with Reno and Vegas - Reno does better since it takes bandwidth from Vegas
  - This is because the goal of Reno is to fill up the queues as quick as possible then the RTT for Vegas increases so Vegas connections decrease their cwnd
- This same idea was also seen in the BBR papers I read in the past
  - BBR would take bandwidth from connections if the BBR connection has a high RTT since it is a more aggressive algorithm


# Fast TCP: From Theory to Experiments
