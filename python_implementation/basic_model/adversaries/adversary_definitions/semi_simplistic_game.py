from data_types import PartyId
from data_types import get_protocol_description

from basic_model import StandardFunctionality
from basic_model import LazyAdversary
from basic_model import ProtocolParty

from network_components import LeakyBuffer
from network_components import ParentParty
from network_components import Environment
from network_components import trusted_setup

from adversarial_actions import CorruptParty
from adversarial_actions import PeekIncomingBuffer
from adversarial_actions import PeekOutgoingBuffer
from adversarial_actions import ClockIncomingBuffer
from adversarial_actions import ClockOutgoingBuffer
from adversarial_actions import SendIncomingMessage
from adversarial_actions import SendOutgoingMessage
from adversarial_actions import QueryFunctionality
from adversarial_actions import InvokeEnvironment

from typing import Set
from typing import Dict

n: int = 2
k: int = 2

# Generate protocol parameters
parameter_set = trusted_setup()
protocol_description = get_protocol_description()

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
incoming_buffers: Dict[int, Dict[int, LeakyBuffer]] = {i: {j: LeakyBuffer() for j in range(k + 1)} for i in range(n)}
outgoing_buffers: Dict[int, Dict[int, LeakyBuffer]] = {i: {j: LeakyBuffer() for j in range(k + 1)} for i in range(n)}

# Variables needed to capture the definition of semi-simplistic adversaries
is_semi_simplistic: bool = True
corrupted_parties: Set[PartyId] = set()

# Complete execution
prev_action = None
next_action = adversary.next_action(None)
while next_action is not None:
    if isinstance(next_action, CorruptParty):
        corrupted_parties.add(next_action.party)
        reply = protocol_parties[next_action.party].corrupt_party()
        prev_action = next_action
        next_action = adversary.next_action(reply)
    elif isinstance(next_action, PeekIncomingBuffer):
        tag = incoming_buffers[next_action.party][next_action.functionality].peek_message(next_action.msg_index)
        prev_action = next_action
        next_action = adversary.next_action(tag)
    elif isinstance(next_action, PeekOutgoingBuffer):
        tag = outgoing_buffers[next_action.party][next_action.functionality].peek_message(next_action.msg_index)
        prev_action = next_action
        next_action = adversary.next_action(tag)
    elif isinstance(next_action, ClockIncomingBuffer):
        # Test that all incoming buffers are flushed
        if next_action.party not in corrupted_parties:
            for corrupted_party in corrupted_parties:
                for buffer in incoming_buffers[corrupted_party].values():
                    if not buffer.empty:
                        is_semi_simplistic = False

        msg = incoming_buffers[next_action.party][next_action.functionality].clock_message(next_action.msg_index)
        write_instructions, reply = protocol_parties[next_action.party](next_action.functionality, msg)
        for port, msg in write_instructions:
            outgoing_buffers[next_action.party][port].write_message(msg)
        prev_action = next_action
        next_action = adversary.next_action(reply)

        # Test that input is forwarded to interpreter when party is corrupted
        if prev_action.party in corrupted_parties:
            if not isinstance(next_action, SendIncomingMessage):
                is_semi_simplistic = False
            else:
                if next_action.functionality != prev_action.functionality:
                    is_semi_simplistic = False
                if next_action.msg != msg:
                    is_semi_simplistic = False
    elif isinstance(next_action, ClockOutgoingBuffer):
        # Test that all incoming buffers are flushed
        if next_action.party not in corrupted_parties:
            for corrupted_party in corrupted_parties:
                for buffer in incoming_buffers[corrupted_party].values():
                    if not buffer.empty:
                        is_semi_simplistic = False

        msg = outgoing_buffers[next_action.party][next_action.functionality].clock_message(next_action.msg_index)
        if next_action.functionality in range(k):
            ideal_functionalities[next_action.functionality](next_action.party, msg)
        else:
            environment(next_action.party, msg)
        prev_action = next_action
        next_action = adversary.next_action(None)
    elif isinstance(next_action, SendIncomingMessage):
        # Previous action must be ClockIncomingBuffer
        if not isinstance(prev_action, ClockIncomingBuffer):
            is_semi_simplistic = False

        write_instructions, reply = protocol_parties[next_action.party].write_to_interpreter(next_action.functionality, next_action.msg)
        for port, msg in write_instructions:
            outgoing_buffers[next_action.party][port].write_message(msg)
        prev_action = next_action
        next_action = adversary.next_action(reply)
    elif isinstance(next_action, SendOutgoingMessage):
        write_instructions = protocol_parties[next_action.party].write_to_outgoing_buffer(next_action.functionality, next_action.msg)
        for port, msg in write_instructions:
            outgoing_buffers[next_action.party][port].write_message(msg)
        next_action = adversary.next_action(None)
    elif isinstance(next_action, InvokeEnvironment):
        reply = environment.adversarial_probe(next_action.msg)
        next_action = adversary.next_action(reply)
    elif isinstance(next_action, QueryFunctionality):
        reply = ideal_functionalities[next_action.target].adversarial_probe(next_action.module, next_action.msg)
        next_action = adversary.next_action(reply)

# Final judgement
print(is_semi_simplistic)
