from network_components import LocalMemory
from network_components import LeakyBuffer

from network_components import InstanceLabel
from network_components import NullInstance
from data_types import InstanceState
from data_types import VolatileState
from data_types import VolatileStateType
from data_types import PinnedLocation

from network_components.adversarial_adapter import AdversarialAdapter

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
    """

    def __init__(self, memory_module: LocalMemory):
        super().__init__()
        self.corrupted: bool = False
        self.memory_module: LocalMemory = memory_module
        self.incoming_buffers: List[LeakyBuffer] = []
        self.outgoing_buffers: List[LeakyBuffer] = []

        self.simulated_incoming_buffers: List[Tuple[InstanceLabel, InstanceLabel, Any]] = []
        self.simulated_outgoing_buffers: List[Tuple[InstanceLabel, InstanceLabel, Any]] = []

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

    # noinspection PyTypeChecker
    def get_volatile_state(self) -> VolatileState:
        """
        Return the current volatile state of the interpreter.
        """
        return self.memory_module.read(
            instance=NullInstance(),
            locations=[(VolatileStateType(), PinnedLocation())])[0]

    def __call__(self, input_port: int, msg: Any) -> Optional[Tuple[int, Any]]:
        """
        Simulates how the corruption module processes inputs from incoming buffers.
        - When the party is honest invokes the interpreter and stops without output.
        - When the party is corrupted returns the input (input port and message) to the adversary.
        - In both cases the output formally goes to the adversary but this is empty when the party is honest.
        """
        volatile_state: VolatileState = self.get_volatile_state()
        if self.corrupted:
            # find out (t1, t2) and take out the corresponding message form simulated incoming port
            # It has to be the outgoimng message in the queue

            return input_port, msg
        else:
            # This part is functionally the same but only notifications go over the
            # but we must simulate the actual messages put into the buffers
            for port, msg in self.interpreter(input_port, msg):
                self.outgoing_buffers[port].write_message(msg)

                # Lets extract the message the interpreter intended to write to the buffer

                # we first need a protocol instance. This is known to the adversary
                # We can get that by making this public
                instance = InstanceLabel()
                program_counter = volatile_state.program_counters[instance]

                # Find out the code line

                # if we have direct addressing read the value from memory

                # if we have indirect addressing read the values by doing indirection

                self.simulated_incoming_buffers # Add stuff into it

            return None

    def corrupt_party(self) -> Tuple[Dict[InstanceLabel, Tuple[ThreadState, int]], Any, Any]:
        """
        Simulates how the corruption module becomes corrupted:
        - Corrupts the party
        - Forces the interpreter to dump their internal state and public and private parameters.
        """
        assert not self.corrupted
        self.corrupted = True
        full_state = self.memory_module.corrupt_party()
        volatile_memory = full_state[NullInstance()][VolatileStateType()][PinnedLocation()]

        state: Dict[InstanceLabel, Tuple[InstanceState, int]] = {}
        for instance, instance_state in full_state:
            if isinstance(instance, NullInstance):
                break
            state[instance] = (full_state[instance], volatile_memory.program_counters[instance])

        return state, volatile_memory.public_param, volatile_memory.private_param

    def write_to_outgoing_buffer(self, input_port: int, msg: Any) -> None:
        """
        Simulates adversarial write to outgoing buffers in the original collection:
        - Adversary can write a message to the outgoing buffers when the party is corrupted.
        - As a result message is written to the desired buffer and the control is given back.
        """
        assert self.corrupted
        assert 0 <= input_port < len(self.outgoing_buffers)

        self.simulated_outgoing_buffers # Add stuff inti it
        #return self.outgoing_buffers[input_port].write_message(msg)
        return None

    def write_to_interpreter(self, input_port: int, msg: Any) -> List[Tuple[int, Any]]:
        """
        Simulates adversarial write to the interpreter in the original collection:
        - Adversary can send a message to the interpreter when the party is corrupted.
        - The input port indicates to the interpreter behalf of whom messages was sent and to whom to send reply.
        - The port numbering matches the numbering of out going buffers:
          * the first k ports correspond to ideal functionalities,
          * and the last port corresponds to the environment.
        - Returns a list of port labels and corresponding messages the interpreter has decided to write into
          outgoing buffers. As the party is corrupted the adversary must decide what to do with this further.
        """
        assert self.corrupted
        assert 0 <= input_port < len(self.outgoing_buffers)

        volatile_state = self.get_volatile_state()

        # Find out the protocol instance
        instance = InstanceLabel()

        program_counter = volatile_state.program_counters[instance]

        # Find out the pending DMA instruction
        # write stuff to the right place in the memory

        # Clock incoming buffer to wake up the interpreter

        # Find out what the interpreter wrote and to where

        # TODO: ??
        return self.interpreter(input_port, msg)

    def clock_incoming_buffer(self):
        pass

    def clock_outgoing_buffer(self):
        pass