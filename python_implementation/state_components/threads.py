from locations import MemoryLocation
from values import ValueType, ValueTypeLabel

from typing import Dict

ThreadState = Dict[ValueTypeLabel, Dict[MemoryLocation, ValueType]]


class ThreadLabel:
    """
    Base class for labelling different threads.
    Thread labels are used inside protocol messages to identify recipient and sender.
    Thread labels are used to index states of interpreters and functionalities.
    """
    pass