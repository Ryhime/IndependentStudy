from Objects.Queue import FIFOQueue
from Objects.Device import Device
from Objects.Packet import Packet
from Objects.Link import Link

class Router(Device):
    queue_size: int
    processing_delay_ms: int
    queue: FIFOQueue
    id: str

    def __init__(self, queue_size: int, processing_delay_ms: int, id: str):
        super().__init__("router", id)
        self.queue_size = queue_size
        self.processing_delay_ms = processing_delay_ms
        self.queue = FIFOQueue()

    def process_tick(self, tick_num: int):
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