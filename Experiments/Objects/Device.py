from abc import ABC, abstractmethod
from Enums.DeviceType import DeviceType
class Device(ABC):
    """Abstract class for a device such as a router or host."""
    device_type: DeviceType
    id: str
    forwarding_table: dict
    links: list

    def __init__(self, device_type: DeviceType, id: str):
        """The constructor for a device.

        Args:
            device_type (DeviceType): The device type
            id (str): The id string of the device
        """
        self.device_type = device_type
        self.id = id
        self.forwarding_table = {}
        self.links = []

    @abstractmethod
    def process_tick(self, tick_num: int):
        pass