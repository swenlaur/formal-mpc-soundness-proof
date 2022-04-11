from data_types import PartyId
from data_types import FunctId
from data_types import InstanceLabel
from data_types import protocol_description

from data_types import CorruptParty
from data_types import PeekIncomingBuffer
from data_types import PeekOutgoingBuffer
from data_types import ClockIncomingBuffer
from data_types import ClockOutgoingBuffer
from data_types import SendIncomingMessage
from data_types import SendOutgoingMessage
from data_types import QueryFunctionality
from data_types import InvokeEnvironment

from basic_model import StandardFunctionality
from basic_model import LazyAdversary
from basic_model import ProtocolParty

from network_components import LeakyBuffer
from network_components import ParentParty
from network_components import Environment
from network_components import trusted_setup


from typing import Any
from typing import Set
from typing import Dict
from typing import Tuple


def get_protocol_instances(msg: Any) -> Tuple[InstanceLabel, InstanceLabel]:
    """
    Extracts protocol instances from outgoing message.
    """
    pass


n: int = 2
k: int = 2

# Generate protocol parameters
parameter_set = trusted_setup()
protocol_description = protocol_description()

parent_parties: Dict[int, ParentParty] = {}  # We do not need them in this model
protocol_parties: Dict[int, ProtocolParty] = {}

# Set up environment and protocol parties
for i, pk, sk in enumerate(parameter_set[:n]):
    parent_parties[i] = ParentParty(pk, sk)
    protocol_parties[i] = ProtocolParty(pk, sk, protocol_description[i], k + 1)
environment = Environment([parent_parties[i] for i in range(n)])

# Set up ideal functionalities
ideal_functionalities: Dict[int, StandardFunctionality] = {}
for i, pk, sk in enumerate(parameter_set[n:n+k]):
    ideal_functionalities[i] = StandardFunctionality(pk, sk)

# Set up the adversary
public_param, private_param = parameter_set[n + k]
adversary = LazyAdversary(public_param, private_param)

# Initialise protocol wiring. The first index marks protocol party. The second index marks ideal functionality.
incoming_buffers: Dict[PartyId, Dict[FunctId, LeakyBuffer]] = {i: {j: LeakyBuffer() for j in range(k + 1)} for i in range(n)}
outgoing_buffers: Dict[PartyId, Dict[FunctId, LeakyBuffer]] = {i: {j: LeakyBuffer() for j in range(k + 1)} for i in range(n)}

# Variables needed to capture the properties of an adversary
is_lazy: bool = True
is_generic: bool = True
is_coherent: bool = True
is_semi_simplistic: bool = True
corrupted_parties: Set[PartyId] = set()
outgoing_signals: Dict[Tuple[PartyId, FunctId, InstanceLabel, InstanceLabel], bool] = dict()


# Complete execution
prev_action = None
next_action = adversary.next_action(None)
while next_action is not None:
    if isinstance(next_action, CorruptParty):
        # Typing guarantees that the adversarial action is correct
        corrupted_parties.add(next_action.party)
        reply = protocol_parties[next_action.party].corrupt_party()
        prev_action = next_action
        next_action = adversary.next_action(reply)
    elif isinstance(next_action, PeekIncomingBuffer):
        # Typing guarantees that the adversarial action is correct
        tag = incoming_buffers[next_action.party][next_action.functionality].peek_message(next_action.msg_index)
        prev_action = next_action
        next_action = adversary.next_action(tag)
    elif isinstance(next_action, PeekOutgoingBuffer):
        # Typing guarantees that the adversarial action is correct
        tag = outgoing_buffers[next_action.party][next_action.functionality].peek_message(next_action.msg_index)
        prev_action = next_action
        next_action = adversary.next_action(tag)
    elif isinstance(next_action, ClockIncomingBuffer):
        # --------------------------------------------------------------------------------------------------------------
        # Test that incoming buffers of corrupted parties are flushed when incoming buffer is clocked for honest party
        if next_action.party not in corrupted_parties:
            for corrupted_party in corrupted_parties:
                for buffer in incoming_buffers[corrupted_party].values():
                    if not buffer.empty:
                        is_semi_simplistic = False
        # --------------------------------------------------------------------------------------------------------------
        msg = incoming_buffers[next_action.party][next_action.functionality].clock_message(next_action.msg_index)
        write_instructions, reply = protocol_parties[next_action.party](next_action.functionality, msg)
        # Typing guarantees that an honest party never issues invalid write instructions
        for port, msg in write_instructions:
            outgoing_buffers[next_action.party][port].write_message(msg)
        prev_action = next_action
        next_action = adversary.next_action(reply)
        # --------------------------------------------------------------------------------------------------------------
        # Test that input is forwarded to the interpreter when party is corrupted
        if prev_action.party in corrupted_parties:
            if not isinstance(next_action, SendIncomingMessage):
                is_semi_simplistic = False
            elif next_action.functionality != prev_action.functionality or next_action.msg != msg:
                is_semi_simplistic = False
        # --------------------------------------------------------------------------------------------------------------
    elif isinstance(next_action, ClockOutgoingBuffer):
        # --------------------------------------------------------------------------------------------------------------
        # Test that incoming buffers of corrupted parties are flushed when outgoing buffer is clocked for honest party
        if next_action.party not in corrupted_parties:
            for corrupted_party in corrupted_parties:
                for buffer in incoming_buffers[corrupted_party].values():
                    if not buffer.empty:
                        is_semi_simplistic = False
        # --------------------------------------------------------------------------------------------------------------
        msg = outgoing_buffers[next_action.party][next_action.functionality].clock_message(next_action.msg_index)
        # --------------------------------------------------------------------------------------------------------------
        # Test that there was signal form interpreter before and clear the signal
        t1, t2 = get_protocol_instances(msg)
        if not outgoing_signals.get((next_action.party, next_action.functionality, t1, t2), False):
            is_lazy = False
        outgoing_signals[next_action.party, next_action.functionality, t1, t2] = False
        # --------------------------------------------------------------------------------------------------------------
        # For technical reasons it makes sense to include environment into the set of functionalities
        if next_action.functionality in range(k):
            ideal_functionalities[next_action.functionality](next_action.party, msg)
        else:
            environment(next_action.party, msg)
        prev_action = next_action
        next_action = adversary.next_action(None)
    elif isinstance(next_action, SendIncomingMessage):
        # --------------------------------------------------------------------------------------------------------------
        # Test that the previous action was ClockIncomingBuffer
        if not isinstance(prev_action, ClockIncomingBuffer):
            is_semi_simplistic = False
        # --------------------------------------------------------------------------------------------------------------
        write_instructions, reply = protocol_parties[next_action.party].write_to_interpreter(next_action.functionality, next_action.msg)
        # Typing guarantees that an honest party never issues invalid write instructions
        for port, msg in write_instructions:
            outgoing_buffers[next_action.party][port].write_message(msg)
            t1, t2 = get_protocol_instances(msg)
            outgoing_signals[next_action.party, port, t1, t2] = True
        prev_action = next_action
        next_action = adversary.next_action(reply)
    elif isinstance(next_action, SendOutgoingMessage):
        # Typing guarantees that even a corrupted party never issues invalid write instructions
        write_instructions = protocol_parties[next_action.party].write_to_outgoing_buffer(next_action.functionality, next_action.msg)
        for port, msg in write_instructions:
            outgoing_buffers[next_action.party][port].write_message(msg)
        next_action = adversary.next_action(None)
    elif isinstance(next_action, InvokeEnvironment):
        reply = environment.adversarial_probe(next_action.msg)
        next_action = adversary.next_action(reply)
    elif isinstance(next_action, QueryFunctionality):
        # Typing guarantees that even a corrupted party never issues invalid write instructions
        reply = ideal_functionalities[next_action.target].adversarial_probe(next_action.module, next_action.msg)
        next_action = adversary.next_action(reply)

# Final judgement
print(environment.output and is_generic and is_coherent and is_semi_simplistic and is_lazy)
