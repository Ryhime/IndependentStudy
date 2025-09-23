from Objects.Host import Host
from Objects.Router import Router
from Objects.Link import Link
from Objects.Device import Device
from Enums.CongestionControlType import CongestionControlType

class Network:
    """Contains an implementation of a Network object.
    Can be thought of as the SDN controller.
    """
    devices: dict
    links: list[Link]

    def __init__(self):
        """Contructor for the Network object."""
        self.devices = {}
        self.links = []


    def add_host(self, id: str, routing_path: list[str] = [], congestion_control: CongestionControlType = CongestionControlType.RENO):
        """Adds a host to the network.

        Args:
            id (str): The string ID of the host
            routing_path (list[str], optional): The set routing path for the host. Defaults to [].
            congestion_control (CongestionControlType, optional): The congestion control algorithm used for the host. Defaults to CongestionControlType.RENO.
        """
        if id in self.devices:
            return
        self.devices[id] = Host(id, routing_path, congestion_control)
        
    def add_router(self, queue_size: int, processing_delay_ms: int, id: str):
        """Adds a router to the network.

        Args:
            queue_size (int): The queue size of the router
            processing_delay_ms (int): The processing delay of the router in ms
            id (str): The string id of the router
        """
        if id in self.devices:
            return
        self.devices[id] = Router(queue_size, processing_delay_ms, id)

    def add_link(self, link_delay_ms: int, bandwidth_in_bytes: int, loss_rate: float, device_id_one: str, device_id_two: str):
        """Adds a link to the network between two devices.

        Args:
            link_delay_ms (int): The propagation delay in ms
            bandwidth_in_bytes (int): The max bandwidth in bytes
            loss_rate (float): The loss rate of the link as a decimal
            device_id_one (str): The string id of the first device
            device_id_two (str): The string id of the second device

        Raises:
            Exception: If the first device does not exist
            Exception: If the second device does not exist
        """
        if device_id_one not in self.devices:
            raise Exception("Device" + str(device_id_one) + "does not exist")
        if device_id_two not in self.devices:
            raise Exception("Device" + str(device_id_two) + "does not exist")
        
        d1: Device = self.devices[device_id_one]
        d2: Device = self.devices[device_id_two]

        link = Link(link_delay_ms, bandwidth_in_bytes, loss_rate, d1, d2)
        self.links.append(link)

        d1.forwarding_table[device_id_two] = link
        d2.forwarding_table[device_id_one] = link
