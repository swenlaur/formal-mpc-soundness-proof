from machine import Machine

from typing import Any
from typing import List


class Environment(Machine):
    """
    Empty base class for all environments.
    """

    def __init__(self, parent_parties: List[Machine]):
        self.parent_parties: List[Machine] = parent_parties

    def adversarial_probe(self, msg: Any) -> Any:
        pass

    # noinspection PyPropertyDefinition
    @property
    def output(self):
        pass
