class Packet:
    """Implements a Packet class."""
    packet_size_bytes: int
    processing_time: int
    id_sequence: list
    original_path: list
    seq_num: int
    ack_num: int
    is_ack: bool
    source_id: str
    dest_id: str
    retransmit_count: int

    def __init__(self, id_sequence: list[str], packet_size_bytes: int, seq_num: int = 0, ack_num: int = 0, is_ack: bool = False, source_id: str = "", dest_id: str = ""):
        """Constructor for the Packet object.

        Args:
            id_sequence (list[str]): The sequence of devices to travel.
            packet_size_bytes (int): The size of the packet in bytes
            seq_num (int, optional): The sequence number of the packet. Defaults to 0.
            ack_num (int, optional): The ACK number of an ACK packet. Defaults to 0.
            is_ack (bool, optional): If the packet is an ACK packet. Defaults to False.
            source_id (str, optional): The string id of the host that sent the packet. Defaults to "".
            dest_id (str, optional): The string id of the destination device. Defaults to "".
        """
        self.id_sequence = id_sequence
        self.original_path = id_sequence.copy()  # For retransmission
        self.processing_time = 0
        self.packet_size_bytes = packet_size_bytes
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.is_ack = is_ack
        self.source_id = source_id
        self.dest_id = dest_id
        self.retransmit_count = 0