from network_components import InputPort
from network_components import OutputPort
from functinality_state import FunctionalityState

from typing import List


class StandardFunctionality:
    port_count: int

    def __init__(self):
        self.state: FunctionalityState = FunctionalityState()
        self.output_ports: List[OutputPort] = [None] * self.port_count

    def connect_buffers(self, input_buffers, output_buffers):
        pass

    def __call__(self, *args, **kwargs) -> List[OutputPort]:
        pass
