from dataclasses import dataclass

from .adversarial_action import AdversarialAction

from typing import Any


@dataclass
class InvokeEnvironment(AdversarialAction):
    msg: Any
