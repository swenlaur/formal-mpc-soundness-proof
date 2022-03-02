from dataclasses import dataclass
from network_components import Machine

from typing import Any


@dataclass
class InputPort:
    machine: Machine
    port_label: Any


@dataclass
class OutputPort:
    machine: Machine
    port_label: Any
