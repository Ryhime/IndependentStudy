from Objects.Queue import FIFOQueue
from Objects.Device import Device
from Objects.Packet import Packet
from Objects.Link import Link
from abc import abstractmethod

class Router(Device):
    """Implementation of a Router."""
    queue_size: int
    processing_delay_ms: int
    queue: FIFOQueue
    id: str

    def __init__(self, queue_size: int, processing_delay_ms: int, id: str):
        """Constructor for a router.

        Args:
            queue_size (int): The queue size in number of packets
            processing_delay_ms (int): The processing delay of the router in ms
            id (str): The string id of the router
        """
        super().__init__("router", id)
        self.queue_size = queue_size
        self.processing_delay_ms = processing_delay_ms
        self.queue = FIFOQueue()

    @abstractmethod
    def process_tick(self, tick_num: int):
        """Called each tick of the simulation.
        Forwards a packet each tick

        Args:
            tick_num (int): The current tick number of the simulation
        """
        while (self.queue.length() > self.queue_size):
            self.queue.queue.pop(-1)

        packet: Packet = self.queue.peak()
        if (packet == None):
            return
        packet.processing_time-=1
        if packet.processing_time <= 0:
            print(self.id, self.forwarding_table)
            if self.id == "r2":
                print(self.forwarding_table["h3"].router_out.id)
                print(self.forwarding_table["h3"].router_in.id)
                print("==========")
            to_send_to: Link = self.forwarding_table[packet.id_sequence[0]]
            packet.processing_time = to_send_to.delay_ms
            to_send_to.packets.append(packet)
            self.queue.pop()