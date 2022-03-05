from network_components import OutputPort
from state_components.functinality_state import FunctionalityState

from typing import Any
from typing import List


class StandardFunctionality:
    port_count: int

    def __init__(self):
        self.state: FunctionalityState = FunctionalityState()
        self.output_ports: List[OutputPort] = [None] * self.port_count

    def __call__(self, *args, **kwargs) -> List[OutputPort]:
        pass

    def adversarial_probe(self, msg: Any) -> Any:
        pass
