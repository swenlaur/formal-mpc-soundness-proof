from locations import MemoryLocation
from values import ValueType, ValueTypeLabel

from typing import Dict

InstanceState = Dict[ValueTypeLabel, Dict[MemoryLocation, ValueType]]

