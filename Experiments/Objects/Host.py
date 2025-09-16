from Objects.Device import Device
from Objects.Packet import Packet
from Objects.Link import Link
from Objects.CongestionControl import RenoCongestionControl, BBRCongestionControl

class Host(Device):
    next_seq_num: int
    unacked_packets: dict  # seq_num -> (packet, send_tick, retransmit_count)
    congestion_control: object  # Congestion control algorithm instance

    def __init__(self, id: str, congestion_control: str = "reno"):
        super().__init__("host", id)
        self.next_seq_num = 0
        self.unacked_packets = {}
        
        # Initialize congestion control
        if congestion_control.lower() == "bbr":
            self.congestion_control = BBRCongestionControl()
        else:
            self.congestion_control = RenoCongestionControl()
        
        self.file = open(self.id, "w")

    def send_packet(self, p: Packet):
        first_hop = p.id_sequence[0]
        if first_hop not in self.forwarding_table:
            raise Exception(f"Invalid path of packet from a host: first_hop {first_hop} not in forwarding table. Available keys: {list(self.forwarding_table.keys())}")
        to_send_link: Link = self.forwarding_table[first_hop]
        to_send_link.packets.append(p)

    def send_data_packet(self, dest_host_id: str, data_size: int, current_tick: int):
        """Send a data packet with congestion control"""
        if len(self.unacked_packets) >= self.congestion_control.get_cwnd():
            return  # Congestion window full

        # Create path for the packet (simplified: assume we know the path to dest)
        path = ["r1", "h2"]
        seq_num = self.next_seq_num
        self.next_seq_num += 1

        p = Packet(
            id_sequence=path,
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
        """Handle incoming ACK packet"""
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
            new_cwnd = self.congestion_control.on_dup_ack(ack_num, current_tick)
            if new_cwnd is not None:
                # Fast retransmit triggered
                self.retransmit_packet(ack_num + 1, current_tick)
                print(f"Host {self.id} fast retransmit seq {ack_num + 1}, cwnd={new_cwnd:.2f}")

    def check_timeouts(self, current_tick: int):
        """Check for packet timeouts and retransmit if needed"""
        for seq_num, (packet, send_tick, retransmit_count) in list(self.unacked_packets.items()):
            if current_tick - send_tick > self.congestion_control.get_rto():
                # Timeout occurred
                new_cwnd = self.congestion_control.on_timeout(seq_num, current_tick)
                self.retransmit_packet(seq_num, current_tick)
                print(f"Host {self.id} timeout for seq {seq_num}, cwnd={new_cwnd:.2f}")

    def retransmit_packet(self, seq_num: int, current_tick: int):
        """Retransmit a specific packet"""
        if seq_num in self.unacked_packets:
            packet, old_send_tick, retransmit_count = self.unacked_packets[seq_num]
            packet.retransmit_count += 1
            # Reset the path to original for retransmission
            packet.id_sequence = packet.original_path.copy()
            self.unacked_packets[seq_num] = (packet, current_tick, retransmit_count + 1)
            self.send_packet(packet)
            print(f"Host {self.id} retransmitted seq {seq_num}")

    def receive_packet(self, packet: Packet, current_tick: int):
        """Handle incoming packets (both data and ACK)"""
        if packet.is_ack:
            self.handle_ack(packet, current_tick)
        else:
            # For data packets, we just acknowledge them (handled in Link)
            pass  # ACK generation is handled in Link class

    def process_tick(self, tick_num: int):
        # Check for timeouts
        self.check_timeouts(tick_num)

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