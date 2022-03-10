from dataclasses import dataclass

from .adversarial_action import AdversarialAction


@dataclass
class CorruptParty(AdversarialAction):
    party: int
