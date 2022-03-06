from typing import Any
from typing import Tuple

from network_components import InstanceLabel


class ReconstructionModule:
    def __init__(self, public_param: Any, private_param: Any):
        self.public_param: Any = public_param
        self.private_param: Any = private_param

        self.state: Dict[InstanceLabel, Tuple[InstanceState, int]] = {}

    def __call__(self, input_port: int, instance: InstanceLabel, data: Any) -> Tuple[bool, Any]:
        pass

    def adversarial_probe(self,  instance: InstanceLabel, data: Any) -> Tuple[bool, Any]:
        pass
