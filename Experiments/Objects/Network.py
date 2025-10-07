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
    throughput_stats: dict
    total_packets_delivered: int
    total_bytes_delivered: int
    simulation_start_tick: int
    def __init__(self):
        """Contructor for the Network object."""
        self.devices = {}
        self.links = []
        self.throughput_stats = {}
        self.total_packets_delivered = 0
        self.total_bytes_delivered = 0
        self.simulation_start_tick = 0


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

        link = Link(link_delay_ms, bandwidth_in_bytes, loss_rate, d1, d2, self)
        self.links.append(link)

        d1.forwarding_table[device_id_two] = link
        d2.forwarding_table[device_id_one] = link

    def record_packet_delivery(self, packet_size_bytes: int, current_tick: int):
        """Record a packet delivery for throughput calculation.
        
        Args:
            packet_size_bytes (int): Size of the delivered packet in bytes
            current_tick (int): Current simulation tick
        """
        self.total_packets_delivered += 1
        self.total_bytes_delivered += packet_size_bytes
        
        # Calculate and store throughput for this interval
        if current_tick > self.simulation_start_tick:
            elapsed_ticks = current_tick - self.simulation_start_tick
            current_throughput = (self.total_bytes_delivered * 8) / elapsed_ticks  # bits per tick
            self.throughput_stats[current_tick] = current_throughput

    def get_average_throughput(self, current_tick: int) -> float:
        """Calculate average throughput in bits per second.
        
        Args:
            current_tick (int): Current simulation tick
            
        Returns:
            float: Average throughput in bits per second
        """
        if current_tick <= self.simulation_start_tick or len(self.throughput_stats) == 0:
            return 0.0
        
        # Convert from bits per tick to bits per second (assuming 1 tick = 1ms)
        total_throughput = sum(self.throughput_stats.values())
        average_throughput_bps = (total_throughput / len(self.throughput_stats)) * 1000
        
        return average_throughput_bps

    def get_current_throughput(self, current_tick: int) -> float:
        """Calculate current throughput in bits per second.
        
        Args:
            current_tick (int): Current simulation tick
            
        Returns:
            float: Current throughput in bits per second
        """
        if current_tick <= self.simulation_start_tick or self.total_bytes_delivered == 0:
            return 0.0
        
        elapsed_ticks = current_tick - self.simulation_start_tick
        # Convert from bytes per tick to bits per second (assuming 1 tick = 1ms)
        current_throughput_bps = ((self.total_bytes_delivered * 8) / elapsed_ticks) * 1000
        
        return current_throughput_bps
