from locations import MemoryLocation
from values import ValueType, ValueTypeLabel

from typing import Dict

InstanceState = Dict[ValueTypeLabel, Dict[MemoryLocation, ValueType]]


class InstanceLabel:
    """
    Base class for labelling different protocol instances.
    Instance labels are used inside protocol messages to identify recipient and sender.
    Instance labels are used to index states of interpreters and functionalities.
    """
    pass
