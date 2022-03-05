from dataclasses import dataclass

from basic_action import AdversarialAction

from typing import Any


@dataclass
class InvokeEnvironment(AdversarialAction):
    msg: Any

