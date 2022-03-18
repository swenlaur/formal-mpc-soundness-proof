from network_components import Machine

from data_types import ValueType
from data_types import ValueTypeLabel
from data_types import MemoryLocation
from data_types import InstanceState
from data_types import InstanceLabel


from typing import Dict
from typing import List
from typing import Tuple


class LocalMemory(Machine):

    def __init__(self):
        """
        The local memory is jointly controlled by the stateless interpreter, the idealised functionalities and
        the adversary. For convenience the adversarial adaptor module can issue specific corruption calls.
        As the volatile state of the interpreter is mapped to the memory, the adversary has access to the volatile
        state of the interpreter through memory reads.
        """
        super().__init__()
        self.corrupted = False
        self.state: Dict[InstanceLabel, InstanceState] = {}

    def write(self,
              instance: InstanceLabel,
              locations: List[Tuple[ValueTypeLabel, MemoryLocation]],
              values: List[ValueType]) -> None:
        """
        Writes values to the specified memory locations.
        If needed initialises sub-states for new protocol instances or memory segments for new value types.
        """
        assert len(locations) == len(values)
        sub_state = self.state.get(instance, {})
        for v_type, v_loc, value in zip(locations, values):
            memory_segment = sub_state.get(v_type, {})
            memory_segment[v_loc] = value

    def read(self,
             instance: InstanceLabel,
             locations: List[Tuple[ValueTypeLabel, MemoryLocation]]) -> List[ValueType]:
        """
        Reads values from the specified memory locations.
        Assumes that all memory addresses are correct.
        """
        assert instance in self.state
        reply = []
        for v_type, v_loc in locations:
            assert v_type in self.state[instance]
            assert v_loc in self.state[instance][v_type]
            reply.append(self.state[instance][v_type][v_loc])
        return reply

    def corrupt_party(self) -> Dict[InstanceLabel, InstanceState]:
        """
        Corrupts the party and forces the interpreter to dump their internal state.
        Note that the volatile state describing the private variables of the interpreter is also mapped to the memory.
        """
        assert not self.corrupted
        self.corrupted = True
        return self.state
