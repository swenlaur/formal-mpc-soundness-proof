from network_components import LeakyBuffer
from network_components import InstanceLabel

from typing import Any
from typing import List


class SharingModule:
    def __init__(self, public_param: Any, private_param: Any):
        self.public_param: Any = public_param
        self.private_param: Any = private_param
        self.outgoing_buffers: List[LeakyBuffer] = []

    def __call__(self, instance: InstanceLabel, caller_instance:InstanceLabel, data: Any) -> Any:
        pass

    def adversarial_probe(self,  instance: InstanceLabel, caller_instance:InstanceLabel, data: Any) -> Any:
        pass

