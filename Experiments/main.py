import json
import time
from Objects.Network import Network

NETWORK_CONFIG = "Configs/Bus.json"

def add_router_to_network(network: Network, device_data: dict):
    """Adds a router to the Network object.

    Args:
        network (Network): The Network object to add to
        device_data (dict): The device data of the router read from the JSON config
    """
    network.add_router(device_data["queue_size"], device_data["processing_delay_ms"], device_data["id"])

def add_host_to_network(network: Network, device_data: dict):
    """Adds a host to the Network object.

    Args:
        network (Network): The Network object to add to
        device_data (dict): The device data of the host read from the JSON config
    """
    congestion_control = device_data.get("congestion_control", "reno")
    routing_path = device_data.get("packet_path", [])
    network.add_host(device_data["id"], routing_path, congestion_control)

def add_link_to_network(network: Network, link_data: dict):
    """Adds a link to the Network.

    Args:
        network (Network): The Network object to add to
        link_data (dict): The link data read from the JSON config
    """
    network.add_link(link_data["link_delay_ms"], link_data["bandwidth_in_bytes"], link_data["loss_rate"], link_data["device_one"]["id"], link_data["device_two"]["id"])


j = open(NETWORK_CONFIG, "r")

data = json.load(j)
network = Network()

# Extract links from the new config structure
links = data.get("links", [])

for link in links:
    d1 = link["device_one"]
    d2 = link["device_two"]

    if d1["type"] == "host":
        add_host_to_network(network, d1)
    else:
        add_router_to_network(network, d1)

    if d2["type"] == "host":
        add_host_to_network(network, d2)
    else:
        add_router_to_network(network, d2)

    add_link_to_network(network, link)


# Set simulation start tick
network.simulation_start_tick = 0

# Main loop
tick_num = 0
max_ticks = 90000
while tick_num < max_ticks:
    time.sleep(.001)
    tick_num += 1
    for d in network.devices.values():
        d.process_tick(tick_num)
    
    for l in network.links:
        l.process_tick(tick_num)
    
    # Log average throughput every 100 ticks
    if tick_num % 100 == 0:
        avg_throughput = network.get_average_throughput(tick_num)
        current_throughput = network.get_current_throughput(tick_num)
        print(f"Tick {tick_num}: Average throughput = {avg_throughput:.2f} bps, Current throughput = {current_throughput:.2f} bps, Total packets delivered = {network.total_packets_delivered}")
