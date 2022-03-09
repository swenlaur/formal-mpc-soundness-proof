from state_components import Queue
from state_components import InstanceLabel
from state_components import InstanceState

from typing import Any
from typing import List
from typing import Tuple
from typing import Dict


class StatefulInterpreter:
    """
    Interpreter can use public and private parameters to interpret code.
    The code is protocol specific but it can be set only once.
    The interpreter can execute several protocol instances with separate states.
    Interpreter will be controlled by the corruption module who invokes it and patches its output
    """

    def __init__(self, public_param: Any, private_param: Any, code: Any, port_count: int):
        self.public_param: Any = public_param
        self.private_param: Any = private_param

        self.code = code
        self.state: Dict[InstanceLabel, Tuple[InstanceState, int]] = {}
        self.input_queues: List[Queue] = [Queue()] * port_count

    def __call__(self, input_port: int, msg: Any) -> List[Tuple[int, Any]]:
        """
        Processes messages coming form ideal functionalities or the environment.
        Returns a list of port labels and corresponding messages the interpreter wants to write to buffers.
        The port numbering matches the numbering of out going buffers:
        * the first k ports correspond to ideal functionalities,
        * and the last port corresponds to the environment.
        """
        assert 0 <= input_port < len(self.input_queues)
        self.input_queues.append[input_port].add(msg)
        protocol_instance: InstanceLabel = self.get_protocol_instance(msg)

        # TODO: add interpreter code here!
        pass

    def reveal_state(self) -> Tuple[Dict[InstanceLabel, Tuple[ThreadState, int]], Any, Any]:
        """Reveals the state together with corresponding program counters and public and private parameters."""
        return self.state, self.public_param, self.private_param

    @staticmethod
    def get_protocol_instance(msg: Any) -> InstanceLabel:
        """
        Extracts protocol instance from the incoming message.
        """
        pass

