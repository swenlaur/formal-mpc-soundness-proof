from dataclasses import dataclass

from .adversarial_action import AdversarialAction


@dataclass
class ClockIncomingBuffer(AdversarialAction):
    source: int
    target: int
    msg_index: int


@dataclass
class ClockOutgoingBuffer(AdversarialAction):
    source: int
    target: int
    msg_index: int
