from network_components import Machine
from network_components import LeakyBuffer
from basic_model import StatefulInterpreter

from typing import Any
from typing import List
from typing import Tuple
from typing import Optional


class CorruptionModule(Machine):
    """
    Corruption module controls how the interpreter interacts with outside world.
    The module writes messages only to outgoing buffers or send them instantly to the adversary.
    """

    def __init__(self, interpreter: StatefulInterpreter):
        self.corrupted = False
        self.outgoing_buffers: List[LeakyBuffer] = []
        self.interpreter: StatefulInterpreter = interpreter

    def __call__(self, input_port: int, msg: Any) -> Optional[Tuple[int, Any]]:
        """
        Processes inputs from incoming buffers.
        When the party is honest invokes the interpreter and stops without output.
        When the party is corrupted returns the input (input port and message) to the adversary.
        In both cases the output formally goes to the adversary but this is empty when the party is honest.
        """
        if self.corrupted:
            return input_port, msg
        else:
            for port, msg in self.interpreter(input_port, msg):
                self.outgoing_buffers[port].write_message(msg)
            return None

    def write_to_outgoing_buffer(self, input_port: int, msg: Any) -> None:
        """
        Adversary can write a message to the outgoing buffers when the party is corrupted.
        As a result message is written to the desired buffer and the control is given back.
        """
        assert self.corrupted
        assert 0 <= input_port < len(self.outgoing_buffers)
        return self.outgoing_buffers[input_port].write_message(msg)

    def write_to_interpreter(self, input_port: int, msg: Any) -> List[Tuple[int, Any]]:
        """
        Adversary can send a message to the interpreter when the party is corrupted.
        The input port determines how the interpreter treats the input:
        0     -- write as an adversary
        1...k -- write as an ideal functionality
        k + 1 -- write as an parent party from the environment

        Returns a list of port labels and corresponding messages the interpreter has decided to write into
        outgoing buffers. As the party is corrupted the adversary must decide what to do with this further.
        """
        assert self.corrupted
        return self.interpreter(input_port, msg)
