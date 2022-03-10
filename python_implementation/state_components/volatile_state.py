from dataclasses import dataclass
from dataclasses import field

from network_components import Queue
from network_components import InstanceLabel

from .values import ValueType
from .values import ValueTypeLabel

from typing import Any
from typing import Dict
from typing import List


@dataclass
class VolatileState(ValueType):
    code: Any = None
    public_param: Any = None
    private_param: Any = None
    input_queues: List[Queue] = field(default_factory=list)
    program_counters: Dict[InstanceLabel, int] = field(default_factory=dict)


class VolatileStateType(ValueTypeLabel):
    pass
