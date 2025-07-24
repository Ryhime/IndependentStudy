class Packet:
    packet_size_bytes: int
    processing_time: int
    id_sequence: list

    def __init__(self, id_sequence: list[str], packet_size_bytes: int):
        self.id_sequence = id_sequence
        self.processing_time = 0
        self.packet_size_bytes = packet_size_bytes