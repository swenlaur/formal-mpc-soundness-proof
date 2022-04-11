from data_types import InstanceLabel
from data_types import InstanceState
from data_types import WriteInstructions
from data_types import FunctId

from network_components import Machine
from basic_model import StatefulInterpreter
from adversarial_failures import InvalidAdversarialAction

from typing import Any
from typing import Dict
from typing import Tuple
from typing import Optional


class ProtocolParty(Machine):
    """
    Protocol party controls how the interpreter interacts with outside world.
    The module uses write-instructions to specify how messages are written to outgoing buffers.
    The module can also write direct messages to the adversary.
    To set up a corruption module the setup parameters must be passed form the trusted setup.

    In the original proof the protocol party is a collection of two machines: interpreter and corruption module.
    Here we formalise the behaviour of the collection without explicit definition of corruption module.
    This makes it easier to formalise the behavior in terms pure functions.
    """

    def __init__(self,  public_param: Any, private_param: Any, code: Any, port_count: int):
        self.corrupted = False
        self.interpreter: StatefulInterpreter = StatefulInterpreter(public_param, private_param, code, port_count)

    def __call__(self, input_port: int, msg: Any) -> Tuple[WriteInstructions, Optional[Tuple[int, Any]]]:
        """
        Processes inputs from incoming buffers and returns a pair of inputs:
        * write-instructions for outgoing buffers;
        * optional reply for the adversary.

        When the party is honest invokes the interpreter and stops without adversarial output.
        When the party is corrupted returns the input (input port and message) to the adversary.
        In both cases the second element of the output goes to the adversary but this is empty when the party is honest.
        """
        if self.corrupted:
            return list(), (input_port, msg)
        else:
            return self.interpreter(input_port, msg), None

    def corrupt_party(self) -> Tuple[Dict[InstanceLabel, Tuple[InstanceState, int]], Any, Any]:
        """
        Corrupts the party and forces the interpreter to dump their internal state and public and private parameters.
        We formally allow double corruption although this deserves special attention during a simulation.
        """
        self.corrupted = True
        return self.interpreter.reveal_state()

    def write_to_outgoing_buffer(self, output_port: FunctId, msg: Any) -> WriteInstructions:
        """
        Adversary can write a message to the outgoing buffers when the party is corrupted.
        As a result corresponding write-instructions for outgoing buffers are returned.
        After that the message is written to the desired buffer and the control is given back to the adversary.
        Note that the typing guarantees that the adversary cannot write to invalid port.
        """
        if not self.corrupted:
            raise InvalidAdversarialAction('Party must be corrupted before sending writing instructions')

        return [(output_port, msg)]

    def write_to_interpreter(self, input_port: int, msg: Any) -> WriteInstructions:
        """
        Adversary can send a message to the interpreter when the party is corrupted.
        The input port indicates to the interpreter behalf of whom messages was sent and to whom to send reply.
        The port numbering matches the numbering of out going buffers:
        * The first k ports correspond to ideal functionalities.
        * The k-th port corresponds to the environment.

        Returns a list of port labels and corresponding messages the interpreter has decided to write into
        outgoing buffers. As the party is corrupted the adversary must decide what to do with this further.
        """
        if not self.corrupted:
            raise InvalidAdversarialAction('Party must be corrupted before sending writing instructions')

        return self.interpreter(input_port, msg)
