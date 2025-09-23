import json
import time
from Objects.Network import Network

NETWORK_CONFIG = "Configs/Bus.json"

def add_router_to_network(network: Network, device_data: dict):
    network.add_router(device_data["queue_size"], device_data["processing_delay_ms"], device_data["id"])

def add_host_to_network(network: Network, device_data: dict):
    # Extracts congestion_control from device data, default to "reno" if not specified
    congestion_control = device_data.get("congestion_control", "reno")
    network.add_host(device_data["id"], congestion_control)

def add_link_to_network(network: Network, link_data: dict):
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


# Main loop
tick_num = 0
max_ticks = 90000  # Limit for testing
while tick_num < max_ticks:
    time.sleep(.001)
    tick_num += 1
    for d in network.devices.values():
        d.process_tick(tick_num)
    
    for l in network.links:
        l.process_tick(tick_num)
