from dataclasses import dataclass
from network_components import Machine


@dataclass
class InputPort:
    machine: Machine
    port_number: int


@dataclass
class OutputPort:
    machine: Machine
    port_number: int
