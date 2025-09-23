from Enums.CongestionControlType import CongestionControlType
from Objects.Device import Device
from Objects.Packet import Packet
from Objects.Link import Link
from Objects.CongestionControl import CongestionControl, RenoCongestionControl, BBRCongestionControl, VegasCongestionControl
from abc import abstractmethod

class Host(Device):
    """Host implementation extends from Device."""
    next_seq_num: int
    unacked_packets: dict  # seq_num -> (packet, send_tick, retransmit_count)
    congestion_control: CongestionControl

    def __init__(self, id: str, routing_path: list[str] = [], congestion_control: CongestionControlType = CongestionControlType.RENO):
        """Constructor for a Host.

        Args:
            id (str): The string id of the host
            routing_path (list[str], optional): The set routing path of the host to send packets. Defaults to [].
            congestion_control (CongestionControlType, optional): The congestion control algorithm to use. Defaults to CongestionControlType.RENO.

        Raises:
            ValueError: When a non valid congestion control algorithm is picked
        """
        super().__init__("host", id)
        self.next_seq_num = 0
        self.unacked_packets = {}
        
        if congestion_control == CongestionControlType.BBR:
            self.congestion_control = BBRCongestionControl()
        elif congestion_control == CongestionControlType.VEGAS:
            self.congestion_control = VegasCongestionControl()
        elif congestion_control == CongestionControlType.RENO:
            self.congestion_control = RenoCongestionControl()
        else:
            raise ValueError("Not a valid congestion control enum used")
        
        self.routing_path = routing_path
        
        self.file = open(self.id, "w")

    def send_packet(self, packet: Packet):
        """Sends a packet along the set routing path.

        Args:
            packet (Packet): The Packet object to send

        Raises:
            Exception: If the next path taken is not in the forwarding table
        """
        first_hop = packet.id_sequence[0]
        if first_hop not in self.forwarding_table:
            raise Exception(f"Invalid path of packet from a host: first_hop {first_hop} not in forwarding table. Available keys: {list(self.forwarding_table.keys())}")
        to_send_link: Link = self.forwarding_table[first_hop]
        to_send_link.packets.append(packet)

    def send_data_packet(self, dest_host_id: str, data_size: int, current_tick: int):
        """Wrapper for send_packet.
        Sends a packet created with the given data.

        Args:
            dest_host_id (str): The host destination string ID
            data_size (int): The size of the packet
            current_tick (int): The current tick of the simulation
        """
        if len(self.unacked_packets) >= self.congestion_control.get_cwnd() or len(self.routing_path) <= 0:
            return

        seq_num = self.next_seq_num
        self.next_seq_num += 1

        p = Packet(
            id_sequence=self.routing_path,
            packet_size_bytes=data_size,
            seq_num=seq_num,
            source_id=self.id,
            dest_id=dest_host_id
        )

        self.unacked_packets[seq_num] = (p, current_tick, 0)
        self.congestion_control.on_packet_sent(seq_num, current_tick)
        self.send_packet(p)
        print(f"Host {self.id} sent packet seq {seq_num}, cwnd={self.congestion_control.get_cwnd():.2f}")

    def handle_ack(self, ack_packet: Packet, current_tick: int):
        """Handles an incoming ACK packet.

        Args:
            ack_packet (Packet): The ACK Packet object
            current_tick (int): The current tick of the simulation
        """
        ack_num = ack_packet.ack_num

        if ack_num in self.unacked_packets:
            # Remove acknowledged packet
            del self.unacked_packets[ack_num]
            
            # Handle congestion control
            new_cwnd = self.congestion_control.on_ack_received(ack_num, current_tick)
            if new_cwnd is not None:
                print(f"Host {self.id} received ACK for seq {ack_num}, cwnd={new_cwnd:.2f}")

        elif ack_num < max(self.unacked_packets.keys(), default=0):
            # Duplicate ACK
            new_cwnd = self.congestion_control.on_dup_ack(ack_num, current_tick)  # type: ignore
            if new_cwnd is not None:
                # Fast retransmit triggered
                self.retransmit_packet(ack_num + 1, current_tick)
                print(f"Host {self.id} fast retransmit seq {ack_num + 1}, cwnd={new_cwnd:.2f}")

    def check_timeouts(self, current_tick: int):
        """Checks if any of the un-ACKed packets timed out.

        Args:
            current_tick (int): The current tick of the simulation
        """
        for seq_num, (packet, send_tick, retransmit_count) in list(self.unacked_packets.items()):
            if current_tick - send_tick > self.congestion_control.get_rto():
                # Timeout occurred
                new_cwnd = self.congestion_control.on_timeout(seq_num, current_tick)
                self.retransmit_packet(seq_num, current_tick)
                print(f"Host {self.id} timeout for seq {seq_num}, cwnd={new_cwnd:.2f}")

    def retransmit_packet(self, seq_num: int, current_tick: int):
        """Retransmits a packet.

        Args:
            seq_num (int): The sequence number to retransmit
            current_tick (int): The current tick of the simulation
        """
        if seq_num in self.unacked_packets:
            packet, _, retransmit_count = self.unacked_packets[seq_num]
            packet.retransmit_count += 1
            # Reset the path to original for retransmission
            packet.id_sequence = packet.original_path.copy()
            self.unacked_packets[seq_num] = (packet, current_tick, retransmit_count + 1)
            self.send_packet(packet)
            print(f"Host {self.id} retransmitted seq {seq_num}")

    def receive_packet(self, packet: Packet, current_tick: int):
        """Handles receiving a non-ACK packet by a host.

        Args:
            packet (Packet): The received Packet object
            current_tick (int): The current tick of the simulation
        """
        if packet.is_ack:
            self.handle_ack(packet, current_tick)

    @abstractmethod
    def process_tick(self, tick_num: int):
        """Called for each tick during the simulation.

        Args:
            tick_num (int): The current tick number of the simulation
        """
        self.check_timeouts(tick_num)

        # TODO - This needs to be much much less hard coded lol

        # Send data packets if we're a source host
        if self.id == "h1":
            self.send_data_packet("h2", 1, tick_num)
            print("CWND 1: ", self.congestion_control.get_cwnd())
            self.file.write(str(self.congestion_control.get_cwnd()) + "\n")
        if self.id == "h3":
            self.send_data_packet("h2", 1, tick_num)
            print("CWND 2: ", self.congestion_control.get_cwnd())
            self.file.write(str(self.congestion_control.get_cwnd()) + "\n")
        if self.id == "h4":
            self.send_data_packet("h4", 1, tick_num)
            print("CWND 3: ", self.congestion_control.get_cwnd())
            self.file.write(str(self.congestion_control.get_cwnd()) + "\n")