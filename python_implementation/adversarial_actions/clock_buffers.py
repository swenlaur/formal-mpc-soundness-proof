from dataclasses import dataclass

from data_types import PartyId
from data_types import FunctId
from .adversarial_action import AdversarialAction


@dataclass
class ClockIncomingBuffer(AdversarialAction):
    party: PartyId
    functionality: FunctId
    msg_index: int


@dataclass
class ClockOutgoingBuffer(AdversarialAction):
    party: PartyId
    functionality: FunctId
    msg_index: int
