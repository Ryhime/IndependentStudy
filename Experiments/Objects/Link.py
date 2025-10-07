from Objects.Device import Device
from Objects.Packet import Packet
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Objects.Network import Network

class Link:
    """Implementation of a link class between Devices."""
    delay_ms: int
    packets: list[Packet]
    router_out: Device
    router_in: Device
    bandwidth_in_bytes: int
    loss_rate: float

    def __init__(self, delay: int, bandwidth_in_bytes: int, loss_rate: float, router_in: Device, router_out: Device, network: 'Network' = None):
        """Constructor for the Link class.

        Args:
            delay (int): The propagation delay of the link in ms
            bandwidth_in_bytes (int): The max bandwidth of the link in bytes
            loss_rate (float): The packet loss probability as a decimal
            router_in (Device): The Device object on one side of the link
            router_out (Device): The Device object on the other side of the link
            network (Network, optional): Reference to the Network for throughput tracking
        """
        self.delay_ms = delay
        self.bandwidth_in_bytes = bandwidth_in_bytes
        self.router_in = router_in
        self.router_out = router_out
        self.packets = []
        self.loss_rate = loss_rate
        self.network = network

    def process_tick(self, tick_num: int):
        """Called each tick during the simulation.

        Args:
            tick_num (int): The current tick of the simulation

        Raises:
            Exception: If the path could not be found to forward the packet along
        """
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
                    raise Exception("Could not find correct path.")
                
                if (to_send_device.device_type == "host"):
                    print("Arrived at host " + str(to_send_device.id))
                    # Deliver the packet to the host for processing with current tick
                    to_send_device.receive_packet(packet, tick_num)
                    
                    # If this is a data packet (not ACK), generate and send ACK back
                    if not packet.is_ack:
                        # Record packet delivery for throughput calculation
                        if self.network:
                            self.network.record_packet_delivery(packet.packet_size_bytes, tick_num)
                        
                        # Create ACK packet with path back to source
                        # Use the original_path from the data packet to determine the return path
                        routers = packet.original_path[:-1]  # Get all routers from the original path
                        ack_path = routers[::-1]  # Reverse the router order
                        ack_path.append(packet.source_id)  # Add the source host as destination
                        ack_packet = Packet(
                            id_sequence=ack_path,
                            packet_size_bytes=0,  # ACK packets are small
                            seq_num=0,
                            ack_num=packet.seq_num,
                            is_ack=True,
                            source_id=to_send_device.id,
                            dest_id=packet.source_id
                        )
                        # Send ACK back through the network
                        to_send_device.send_packet(ack_packet)
                        print(f"Host {to_send_device.id} generated ACK for seq {packet.seq_num}")
                else:
                    packet.id_sequence = packet.id_sequence[1:len(packet.id_sequence)]
                    packet.processing_time = to_send_device.processing_delay_ms
                    to_send_device.queue.push(packet)
            else:
                i += 1
