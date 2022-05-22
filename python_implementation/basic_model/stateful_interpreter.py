from data_types import InstanceLabel
from data_types import InstanceState
from data_types import WriteInstructions
from data_types.interpreter_messages import INIT
from network_components import Queue
from network_components import Machine
from adversarial_failures import ProtocolFailure
from typing import Any
from typing import List
from typing import Tuple
from typing import Dict


class StatefulInterpreter(Machine):
    """
    Interpreter can use public and private parameters to interpret code.
    The code is protocol specific, but it can be set only once.
    The interpreter can execute several protocol instances with separate states.
    Interpreter will be controlled by the protocol party who invokes it and patches its output
    """

    def __init__(self, public_param: Any, private_param: Any, code: Any, port_count: int):
        self.public_param: Any = public_param
        self.private_param: Any = private_param

        self.code = code #Semantics: program code p
        self.state: Dict[InstanceLabel, Tuple[InstanceState, int]] = {} #"Two-dimensional array capturing the internal state of the interpreter"
        self.port_count = port_count
        self.input_queues: List[Queue] = [Queue()] * port_count #Input ports i

    def __call__(self, input_port: int, msg: Any) -> WriteInstructions:
        """
        Processes messages coming form ideal functionalities or the environment.
        Returns a list of port labels and corresponding messages the interpreter wants to write into buffers.

        The port numbering matches the numbering of outgoing buffers:
        * The 0-th port is adv
        * The first k ports correspond to ideal functionalities.
        * The k-th port corresponds to the environment.

        Johanna: in that case, INIT(t*,m) is sent to the k-th input port?
        """
        if input_port < 0 or self.port_count <= input_port:
            raise ProtocolFailure('Invalid input port')

        self.input_queues[input_port].add(msg)
        protocol_instance: InstanceLabel = self.get_protocol_instance(msg)
        writing_instructions: WriteInstructions = [] #Output messages o

        # TODO: add interpreter code here!
        # Explicit assumptions about the interpreter
        # 1) Interpreter never writes to invalid port!
        _ = protocol_instance

        if input_port == 0 and msg == INIT: #Is there a better way than if-then to write up semantics?
            self.input_queues[input_port].add(msg)
            self.state[_] = ({}, 0) # This is supposed to be the empty initialized state, but I don't think the 0 should be there.
            #Which variable is the program counter n?





        return writing_instructions

    def reveal_state(self) -> Tuple[Dict[InstanceLabel, Tuple[InstanceState, int]], Any, Any]:
        """Reveals the state together with corresponding program counters and public and private parameters."""
        return self.state, self.public_param, self.private_param

    @staticmethod
    def get_protocol_instance(msg: Any) -> InstanceLabel:
        """
        Extracts protocol instance from the incoming message.
        """
        pass
