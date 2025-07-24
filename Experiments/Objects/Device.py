class Device:
    device_type: str
    id: str
    forwarding_table: dict

    def __init__(self, device_type: str, id: str):
        self.device_type = device_type
        self.id = id
        self.forwarding_table = {}

    def process_tick(self, tick_num: int):
        pass