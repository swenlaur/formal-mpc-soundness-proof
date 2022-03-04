from dataclasses import dataclass

@dataclass
class ClockIncomingBuffer:
    source: int
    target: int
    msg_index: int

@dataclass
class ClockOutgoingBuffer:
    source: int
    target: int
    msg_index: int


