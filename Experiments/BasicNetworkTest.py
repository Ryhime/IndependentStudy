from Networks import DefaultNetwork, LoopedSwitchesNetwork
from mininet.node import Controller
from mininet.cli import CLI
from mininet.net import Mininet

topo = LoopedSwitchesNetwork()
net = Mininet(topo=topo, controller=Controller)
net.start()
net.pingAll()
net.stop()
