from network_components import Machine
from network_components import LocalMemory
from network_components import LeakyBuffer

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Optional


class DummyAdversarialAdapter(Machine):
    """
    Adversarial adapter that violates all memory access restrictions.
    Just to get going
    """

    def __init__(self, memory_module: LocalMemory):
        super().__init__()
        self.corrupted: bool = False
        self.memory_module: LocalMemory = memory_module
        self.incoming_buffers: List[LeakyBuffer] = []
        self.outgoing_buffers: List[LeakyBuffer] = []

    def set_clockable_buffers(self, incoming_buffers: List[LeakyBuffer], outgoing_buffers: List[LeakyBuffer]):
        """
        To complete the setup one must specify the set of buffers the adversary can clock around the interpreter.
        Note that leaky buffers will be split between many adapter modules and thus the complete execution differs
        slightly fom the original setup. Namely, actions ClockIncomingBuffer and ClockOutgoingBuffer are divided
        between adapter modules so that the right module processes the action.
        """
        self.incoming_buffers = incoming_buffers
        self.outgoing_buffers = outgoing_buffers

    def __call__(self, input_port: int, msg: Any) -> Optional[Tuple[int, Any]]:
        """
        Simulates how the corruption module processes inputs from incoming buffers.
        - When the party is honest invokes the interpreter and stops without output.
        - When the party is corrupted returns the input (input port and message) to the adversary.
        - In both cases the output formally goes to the adversary but this is empty when the party is honest.
        """
        if self.corrupted:
            # TODO: Correct this
            return input_port, msg
        else:
            # TODO: ??
            for port, msg in self.interpreter(input_port, msg):
                self.outgoing_buffers[port].write_message(msg)
            return None

    def corrupt_party(self) -> Tuple[Dict[ThreadLabel, Tuple[ThreadState, int]], Any, Any]:
        """
        Simulates how the corruption module becomes corrupted:
        - Corrupts the party
        - Forces the interpreter to dump their internal state and public and private parameters.
        """
        assert not self.corrupted
        self.corrupted = True
        # TODO: Read memory and reassemble stuff
        return self.interpreter.reveal_state()

    def write_to_outgoing_buffer(self, input_port: int, msg: Any) -> None:
        """
        Simulates adversarial write to outgoing buffers in the original collection:
        - Adversary can write a message to the outgoing buffers when the party is corrupted.
        - As a result message is written to the desired buffer and the control is given back.
        """
        assert self.corrupted
        # TODO: ??
        assert 0 <= input_port < len(self.outgoing_buffers)
        return self.outgoing_buffers[input_port].write_message(msg)

    def write_to_interpreter(self, input_port: int, msg: Any) -> List[Tuple[int, Any]]:
        """
        Simulates adversarial write to the interpreter in the original collection:
        - Adversary can send a message to the interpreter when the party is corrupted.
        - The input port indicates to the interpreter behalf of whom messages was sent and to whom to send reply.
        - The port numbering matches the numbering of out going buffers:
          * the first k ports correspond to ideal functionalities,
          * and the last port corresponds to the environment.
        - Returns a list of port labels and corresponding messages the interpreter has decided to write into
          outgoing buffers. As the party is corrupted the adversary must decide what to do with this further.
        """
        assert self.corrupted
        # TODO: ??
        assert 0 <= input_port < len(self.outgoing_buffers)
        return self.interpreter(input_port, msg)
