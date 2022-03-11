from data_types import ValueType
from data_types import ValueTypeLabel
from data_types import InstanceLabel
from data_types import NullInstance
from data_types import InstanceState
from data_types import PinnedLocation
from data_types import MemoryLocation

from network_components import LocalMemory
from network_components import LeakyBuffer
from network_components import AdversarialAdapter

from .volatile_state import VolatileState
from .volatile_state import VolatileStateType

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Optional


class DummyAdversarialAdapter(AdversarialAdapter):
    """
    Adversarial adapter that violates all memory access restrictions but manages to simulate the original
    protocol execution in the basic model. Meant to get going with the simulation.
    There are small differences in the description of complete execution but these are convenience changes.
    More refined explanations are in function comments.

    Simulation goals:
    - Simulated buffers have the same state as in basic-model
    """

    def __init__(self, memory_module: LocalMemory):
        super().__init__()
        self.corrupted: bool = False
        self.memory_module: LocalMemory = memory_module
        self.incoming_buffers: List[LeakyBuffer] = []
        self.outgoing_buffers: List[LeakyBuffer] = []

        self.simulated_incoming_buffers: List[LeakyBuffer] = []
        self.simulated_outgoing_buffers: List[LeakyBuffer] = []

    def set_clockable_buffers(self, incoming_buffers: List[LeakyBuffer], outgoing_buffers: List[LeakyBuffer]):
        """
        To complete the setup one must specify the set of buffers the adversary can clock around the interpreter.
        Note that leaky buffers will be split between many adapter modules and thus the complete execution differs
        slightly fom the original setup. Namely, actions ClockIncomingBuffer and ClockOutgoingBuffer are divided
        between adapter modules so that the right module processes the action.
        """
        self.incoming_buffers = incoming_buffers
        self.outgoing_buffers = outgoing_buffers
        self.simulated_outgoing_buffers = [LeakyBuffer()] * len(outgoing_buffers)
        self.simulated_incoming_buffers = [LeakyBuffer()] * len(incoming_buffers)

    def get_volatile_state(self) -> VolatileState:
        """
        Return the current volatile state of the interpreter.
        """
        # noinspection PyTypeChecker
        return self.memory_module.read(
            instance=NullInstance(),
            locations=[(VolatileStateType(), PinnedLocation())])[0]

    def get_interpreter_outcome(self) -> List[Tuple[int, Any]]:
        """
        Extracts what messages the interpreter has "written" to the output ports.
        Of course, the interpreter just writes these to memory locations, and thus we must assemble the message.
        For that we need to know the details of last executed instruction:
        - protocol instance
        - sub-protocol instances
        - message locations
        """
        volatile_state: VolatileState = self.get_volatile_state()
        protocol_instance, sub_protocol_instance = volatile_state.last_call
        writes = []
        for output_port, locations in volatile_state.pending_writes[protocol_instance, sub_protocol_instance]:
            writes.append((output_port, self.memory_module.read(protocol_instance, locations)))
        return writes

    def get_outgoing_message_address(self) -> Tuple[InstanceLabel, List[Tuple[ValueTypeLabel, MemoryLocation]]]:
        """
        Extracts where are 
        :return:
        """
        pass

    def corrupt_party(self) -> Tuple[Dict[InstanceLabel, Tuple[InstanceState, int]], Any, Any]:
        """
        Simulates how the corruption module becomes corrupted:
        - Corrupts the party
        - Forces the interpreter to dump their internal state and public and private parameters.
        """
        assert not self.corrupted
        self.corrupted = True
        full_state = self.memory_module.corrupt_party()
        # noinspection PyTypeChecker
        volatile_memory: VolatileState = full_state[NullInstance()][VolatileStateType()][PinnedLocation()]

        state: Dict[InstanceLabel, Tuple[InstanceState, int]] = {}
        for instance, instance_state in full_state:
            if isinstance(instance, NullInstance):
                break
            state[instance] = (full_state[instance], volatile_memory.program_counters[instance])

        return state, volatile_memory.public_param, volatile_memory.private_param

    def clock_incoming_buffer(self, input_port: int, msg_index: int) -> Optional[Tuple[int, Any]]:
        """
        Adversarial adaptor always forward the clocking signal to the DMA reply buffer.
        This activates the corresponding interpreter which then stops and control goes back
        to adversarial adaptor which now has to fake the response from corruption module.
        To keep consistent simulation state the following actions are performed
        - The message is clocked out of the simulated ingoing buffer
        - The corresponding response of the corruption module is simulated
        """
        msg = self.simulated_incoming_buffers[input_port].clock_message(msg_index)
        if not self.corrupted:
            for port, msg in self.get_interpreter_outcome():
                self.simulated_outgoing_buffers[port].write_message(msg)
            return None
        else:
            return input_port, msg

    def clock_outgoing_buffer(self, output_port: int, msg_index: int) -> None:
        """
        Simulates the execution following to the clocking of an outgoing buffer.
        - The message is clocked out of the simulated outgoing buffer
        - Makes sure that the memory locations referenced by the DMA message are overwritten.
        This guarantees that the ideal functionality fetches the same message that comes out form simulated buffer
        """
        msg = self.simulated_outgoing_buffers[output_port].clock_message(msg_index)
        if self.corrupted:
            # Split message and overwrite memory locations
            instance, locations = self.get_outgoing_message_address()
            for v_type, v_loc, value in zip(locations, msg):
                self.memory_module[instance][v_type][v_loc] = value
        return None

    def write_to_outgoing_buffer(self, input_port: int, msg: Any) -> None:
        """
        Simulates adversarial write to outgoing buffers in the original collection.
        As the adaptor corrupts memory locations read by ideal functionalities just before
        messages are clocked to their input ports we can just write messages into simulated buffer.
        """
        assert self.corrupted
        assert 0 <= input_port < len(self.outgoing_buffers)
        self.simulated_outgoing_buffers[int].write_message(msg)
        return None

    def write_to_interpreter(self, input_port: int, msg: Any) -> List[Tuple[int, Any]]:
        """
        Simulates adversarial write to the interpreter in the original collection.
        As the message has already successfully reached the stateless interpreter
        we need to fetch the messages that interpreter has written to the ports.
        """
        assert self.corrupted
        assert 0 <= input_port < len(self.outgoing_buffers)
        return self.get_interpreter_outcome()