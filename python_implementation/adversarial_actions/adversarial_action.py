from dataclasses import dataclass

from data_types import PartyId
from data_types import FunctId
from data_types import InstanceLabel

from typing import Any


class AdversarialAction:
    pass


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


@dataclass
class PeekIncomingBuffer(AdversarialAction):
    party: PartyId
    functionality: FunctId
    msg_index: int


@dataclass
class PeekOutgoingBuffer(AdversarialAction):
    party: PartyId
    functionality: FunctId
    msg_index: int


@dataclass
class CorruptParty(AdversarialAction):
    party: int


@dataclass
class InvokeEnvironment(AdversarialAction):
    msg: Any


@dataclass
class SendOutgoingMessage(AdversarialAction):
    party: PartyId
    functionality: FunctId
    msg: Any


@dataclass
class SendIncomingMessage(AdversarialAction):
    party: PartyId
    functionality: FunctId
    msg: Any


@dataclass
class QueryFunctionality(AdversarialAction):
    target: int
    module: str
    instance: InstanceLabel
    msg: Any
