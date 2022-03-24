from dataclasses import dataclass

from data_types import PartyId
from data_types import FunctId
from .adversarial_action import AdversarialAction


@dataclass
class PeekIncomingBuffer(AdversarialAction):
    source: FunctId
    target: PartyId
    msg_index: int


@dataclass
class PeekOutgoingBuffer(AdversarialAction):
    source: PartyId
    target: FunctId
    msg_index: int
