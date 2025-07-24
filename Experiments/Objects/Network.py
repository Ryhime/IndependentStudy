from Objects.Host import Host
from Objects.Router import Router
from Objects.Link import Link
from Objects.Device import Device

class Network:
    devices: dict
    links: list[Link]

    def __init__(self):
        self.devices = {}
        self.links = []


    def add_host(self, id: str):
        if id in self.devices:
            return None
        self.devices[id] = Host(id)
        
    def add_router(self, queue_size: int, processing_delay_ms: int, id: str):
        if id in self.devices:
            return None
        self.devices[id] = Router(queue_size, processing_delay_ms, id)

    def add_link(self, link_delay_ms: int, bandwidth_in_bytes: int, loss_rate: float, device_id_one: str, device_id_two: str):
        if device_id_one not in self.devices:
            raise("Device" + str(device_id_one) + "does not exist")
        if device_id_two not in self.devices:
            raise("Device" + str(device_id_two) + "does not exist")
        
        d1: Device = self.devices[device_id_one]
        d2: Device = self.devices[device_id_two]

        link = Link(link_delay_ms, bandwidth_in_bytes, loss_rate, d1, d2)
        self.links.append(link)

        d1.forwarding_table[device_id_two] = link
        d2.forwarding_table[device_id_one] = link