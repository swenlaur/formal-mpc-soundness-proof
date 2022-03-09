from network_components import Machine
from network_components import LeakyBuffer
from network_components import InstanceLabel
from network_components import Queue

from typing import List
from typing import Any


class StatelessInterpreter(Machine):
    """
    Interpreter can use public and private parameters to interpret code.
    The code is protocol specific, but it can be set only once.
    The interpreter can execute several protocol instances with separate states.
    Interpreter will be controlled by the corruption module who invokes it and patches its output
    """
    def __init__(self, public_param: Any, private_param: Any, code: Any, port_count: int, memory_module: Machine):
        super().__init__()

        self.code = code
        self.public_param: Any = public_param
        self.private_param: Any = private_param

        self.memory_module: Machine = memory_module
        self.outgoing_buffers: List[LeakyBuffer] = []
        self.input_queues: List[Queue] = [Queue()] * port_count

        self.copy_state_to_memory()

    def __call__(self, input_port: int, msg: Any) -> None:
        """
        Processes input notifications from incoming buffers.
        These messages only identify the protocol instance and responder identity.
        This is enough to locate the corresponding pending instruction in the code and continue.
        The actual execution requires interaction with the memory module.
        The control goes back to the adversary after the interpretation step is completed.
        """
        assert 0 <= input_port < len(self.input_queues)
        self.input_queues[input_port].add(msg)
        protocol_instance: InstanceLabel = self.get_protocol_instance(msg)

        # TODO: add interpreter code here!

        return self.copy_state_to_memory()

    def copy_state_to_memory(self) -> None:
        """
        Copies the interpreter state to the memory.
        """
        pass

    @staticmethod
    def get_protocol_instance(msg: Any) -> InstanceLabel:
        """
        Extracts protocol instance from the incoming message.
        """
        pass
