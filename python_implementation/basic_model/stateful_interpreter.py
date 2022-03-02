from network_components import InputPort
from network_components import OutputPort
from interpreter_state import InterpreterState

from typing import Any
from typing import List


class StatefulInterpreter:

    port_count: int = 2

    def __init__(self, public_param: Any, private_param: Any, code: Any):
        self.input_buffers: List[InputPort] = [None] * self.port_count
        self.output_buffers: List[OutputPort] = [None] * self.port_count
        self.state: InterpreterState = InterpreterState()
        self.pc: List[int] = [None] * self.port_count

    def connect_buffers(self, input_buffers, output_buffers):
        pass

    def __call__(self, *args, **kwargs) -> List[OutputPort]:
        pass
