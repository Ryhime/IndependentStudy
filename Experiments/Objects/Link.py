from Objects.Device import Device
from Objects.Packet import Packet
import random

class Link:
    delay_ms: int
    packets: list[Packet]
    router_out: Device
    router_in: Device
    bandwidth_in_bytes: int
    loss_rate: float

    def __init__(self, delay: int, bandwidth_in_bytes: int, loss_rate: float, router_in: Device, router_out: Device):
        self.delay_ms = delay
        self.bandwidth_in_bytes = bandwidth_in_bytes
        self.router_in = router_in
        self.router_out = router_out
        self.packets = []
        self.loss_rate = loss_rate

    def process_tick(self, tick_num: int):
        # Check for bandwidth
        used_bandwidth: int = sum(list(map(lambda x: x.packet_size_bytes, self.packets)))
        while (used_bandwidth > self.bandwidth_in_bytes and len(self.packets) > 0):
            packet: Packet = self.packets.pop(-1)
            used_bandwidth -= packet.packet_size_bytes

        # Send packets to next device if needed
        i = 0
        while i < len(self.packets):
            packet = self.packets[i]
            if len(packet.id_sequence) <= 0:
                self.packets.pop(i)
                continue
            packet.processing_time -= 1
            if (packet.processing_time <= 0):
                self.packets.pop(i)

                # Lossy Link
                if random.random() <= self.loss_rate:
                    continue

                # Add it to the next device
                to_send_device: Device = None
                if (self.router_in.id == packet.id_sequence[0]):
                    to_send_device = self.router_in
                elif (self.router_out.id == packet.id_sequence[0]):
                    to_send_device = self.router_out
                else:
                    raise("Could not find correct path.")
                
                if (to_send_device.device_type == "host"):
                    print("Arrived at host " + str(to_send_device.id))
                else:
                    packet.id_sequence = packet.id_sequence[1:len(packet.id_sequence)]
                    packet.processing_time = to_send_device.processing_delay_ms
                    to_send_device.queue.push(packet)
            else:
                i += 1