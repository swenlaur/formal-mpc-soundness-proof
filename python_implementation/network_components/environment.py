from .machine import Machine
from .buffers import LeakyBuffer

from typing import Any
from typing import List


class Environment(Machine):
    """
    Empty base class for all environments.
    """

    def __init__(self, parent_parties: List[Machine]):
        self.parent_parties: List[Machine] = parent_parties
        self.outgoing_buffers: List[LeakyBuffer] = []

    def set_outgoing_buffers(self, outgoing_buffers: List[LeakyBuffer]):
        """
        To complete the setup one must specify leaky output buffers towards protocol parties.
        """
        self.outgoing_buffers = outgoing_buffers

    def adversarial_probe(self, msg: Any) -> Any:
        pass


    # noinspection PyPropertyDefinition
    @property
    def output(self):
        pass
