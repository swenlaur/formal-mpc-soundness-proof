from dataclasses import dataclass

from typing import Any


@dataclass
class SendOutgoingMessage:
    source: int
    target: int
    msg: Any


@dataclass
class SendIncomingMessage:
    source: int
    target: int
    msg: Any


@dataclass
class QueryFunctionality:
    target: int
    msg: Any

