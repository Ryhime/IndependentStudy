# Topology
- Only routers are used since simulating switches/broadcasts is out of scope
- Test different sized topologies
  - Does using a LSTM or regular neural network fail after a certain topology size
  - Does a GNN continue to scale with it
- Data set topologies, different base topologies like: star, ring, and mesh

# Generating Artifical Network Traffic
- Packets should simulate TCP and UDP packets
  - TCP should meausre RTT and go both directions
  - TCP packet loss retransmission
  - NO TCP ramp up since it is out of scope
- Nodes represent different types of users
  - Server - Only receives packets
  - Two nodes talking - Send UDP packets to each other
  - Large file transfer - Constant stream of TCP packets
  - Etc - The different network slicing use cases that I can't find anymore...

# Simulating Delays
- Want to capture the following delays:
  - Processing, Queueing, Transmission, and Propagation Delay

# Topology Failures
- Simulate different links going out and turning back on
- A router being removed from the network
- A link being completely removed and not turning back on
