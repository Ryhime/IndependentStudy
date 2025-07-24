from Objects.Device import Device
from Objects.Packet import Packet
from Objects.Link import Link

class Host(Device):

    def __init__(self, id: str):
        super().__init__("host", id)

    def send_packet(self, p: Packet):
        if (p.id_sequence[0] not in self.forwarding_table):
            raise("Invalid path of packet from a host")
        to_send_link: Link = self.forwarding_table[p.id_sequence[0]]
        to_send_link.packets.append(p)

    def process_tick(self, tick_num: int):
        if self.id != "h1":
            return
        p: Packet = Packet(["r1", "r2", "h2"], 1)
        if tick_num % 2 == 0:
            self.send_packet(Packet(["r1", "r2", "h3"], 1))
        # self.send_packet(p)