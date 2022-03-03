from network_components import Machine
from network_components import LeakyBuffer
from basic_model import StatefulInterpreter

from typing import List
from typing import Tuple


class CorruptionModule(Machine):
    """
    Corruption module controls how the interpreter interacts with outside world.
    The module sends messages only to outgoing buffers or instantly to the adversary.
    """

    def __init__(self, interpreter: StatefulInterpreter):
        self.outgoing_buffers: List[LeakyBuffer] = []
        self.interpreter: StatefulInterpreter = interpreter

    def __call__(self, *args, **kwargs) -> Tuple[Machine, int, Any]:
        """Honest calls?"""
        pass
