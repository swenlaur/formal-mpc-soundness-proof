from data_types import InstanceLabel

from typing import Any
from typing import Tuple


class ComputationModule:
    def __init__(self, public_param: Any, private_param: Any):
        self.public_param: Any = public_param
        self.private_param: Any = private_param

    def __call__(self, instance: InstanceLabel, data: Any) -> Tuple[bool, Any]:
        pass
