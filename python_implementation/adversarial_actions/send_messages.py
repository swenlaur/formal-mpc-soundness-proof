from dataclasses import dataclass

from basic_action import AdversarialAction

from typing import Any


@dataclass
class SendOutgoingMessage(AdversarialAction):
    source: int
    target: int
    msg: Any


@dataclass
class SendIncomingMessage(AdversarialAction):
    source: int
    target: int
    msg: Any


@dataclass
class QueryFunctionality(AdversarialAction):
    target: int
    module: str
    msg: Any

