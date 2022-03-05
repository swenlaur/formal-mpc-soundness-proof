from dataclasses import dataclass

from basic_action import AdversarialAction

@dataclass
class CorruptParty(AdversarialAction):
    party: int
