from network_components import LeakyBuffer
from network_components import Queue

from network_components import Machine
from network_components import LocalMemory

from .volatile_state import VolatileState
from .volatile_state import VolatileStateType
from data_types import PinnedLocation
from data_types import InstanceLabel
from data_types import NullInstance

from typing import Any
from typing import List
from typing import Dict


class StatelessInterpreter(Machine):
    """
    Interpreter can use public and private parameters to interpret code.
    The code is protocol specific, but it can be set only once.
    The interpreter can execute several protocol instances with separate states.
    Interpreter will be controlled by the corruption module who invokes it and patches its output
    """
    def __init__(self, public_param: Any, private_param: Any, code: Any, port_count: int, memory_module: LocalMemory):
        super().__init__()
        self.code = code
        self.public_param: Any = public_param
        self.private_param: Any = private_param

        self.memory_module: LocalMemory = memory_module
        self.outgoing_buffers: List[LeakyBuffer] = []
        self.input_queues: List[Queue] = [Queue()] * port_count
        self.program_counters: Dict[InstanceLabel, int] = {}

        self.copy_state_to_memory()

    def set_outgoing_buffers(self, outgoing_buffers: List[LeakyBuffer]):
        """
        TODO: complete this
        To complete the setup one must specify leaky output buffers to ideal functionalities and environment.
        """
        self.outgoing_buffers = outgoing_buffers

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
        _ = protocol_instance

        return self.copy_state_to_memory()

    def copy_state_to_memory(self) -> None:
        """
        Copies the volatile state of the interpreter state to the dedicated section of the memory.
        """
        self.memory_module.write(
            instance=NullInstance(),
            locations=[(VolatileStateType(), PinnedLocation())],
            values=[VolatileState(
                code=self.code,
                public_param=self.public_param,
                private_param=self.private_param,
                input_queues=self.input_queues,
                program_counters=self.program_counters
            )])

    @staticmethod
    def get_protocol_instance(msg: Any) -> InstanceLabel:
        """
        Extracts protocol instance from the incoming message.
        """
        pass
