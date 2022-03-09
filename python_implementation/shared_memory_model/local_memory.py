from network_components import Machine
from network_components import InstanceLabel

from state_components import ValueType
from state_components import ValueTypeLabel
from state_components import MemoryLocation

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple


class LocalMemory(Machine):
    def __init__(self):
        """
        The local memory is jointly controlled by the stateless interpreter and the idealised functionalities.
        Additionally, the adversarial adaptor module can issue specific corruption calls.
        """
        super().__init__()
        self.corrupted = False

    def write(self,
              instance: InstanceLabel,
              locations: List[Tuple[ValueTypeLabel, MemoryLocation]],
              values: List[ValueType]) -> None:
        """
        Writes values to the specified memory locations.

        """
        pass

    def read(self,
             instance: InstanceLabel,
             locations: List[Tuple[ValueTypeLabel, MemoryLocation]]) -> List[ValueType]:
        """
        Reads values from the specified memory locations.
        """
        pass

    def corrupt_party(self) -> Tuple[Dict[ThreadLabel, Tuple[ThreadState, int]], Any, Any]:
        """
        Corrupts the party and forces the interpreter to dump their internal state and public and private parameters.
        """
        assert not self.corrupted
        self.corrupted = True
        return None

    def get_corrupted_interpreter_state(self, instance: InstanceLabel) -> List[ValueType]:
        """
        Adversaries way to get the current state of the interpreter.
        """
        pass

    def read_corrupted_memory(
            self,
            instance: InstanceLabel,
            locations: List[Tuple[ValueTypeLabel, MemoryLocation]]) -> List[ValueType]:
        """
        Adversaries way to read corrupted memory locations.
        """
        pass

    def write_corrupted_memory(
            self,
            instance: InstanceLabel,
            locations: List[Tuple[ValueTypeLabel, MemoryLocation]],
            values: List[ValueType]) -> None:
        """
        Adversaries way to write corrupted memory locations.
        """
        pass
