from dataclasses import dataclass
from data_types import InstanceLabel
from data_types import PartyId
from data_types import FunctId
from .adversarial_action import AdversarialAction

from typing import Any


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

