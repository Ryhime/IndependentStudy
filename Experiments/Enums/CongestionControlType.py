from enum import Enum
class CongestionControlType(str, Enum):
    BBR = "bbr"
    VEGAS = "vegas"
    RENO = "reno"
    RL = "rl"