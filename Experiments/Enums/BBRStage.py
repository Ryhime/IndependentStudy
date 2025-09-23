from enum import Enum
class BBRStage(Enum):
    STARTUP = 1
    DRAIN = 2
    PROB_BW = 3
    PROB_RTT = 4