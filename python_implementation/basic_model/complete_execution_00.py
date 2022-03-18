from data_types import protocol_description

from basic_model import StandardFunctionality
from basic_model import LazyAdversary
from basic_model import ProtocolParty

from network_components import LeakyBuffer
from network_components import ParentParty
from network_components import Environment
from network_components import trusted_setup

from adversarial_actions import CorruptParty
from adversarial_actions import ClockIncomingBuffer
from adversarial_actions import ClockOutgoingBuffer
from adversarial_actions import SendIncomingMessage
from adversarial_actions import SendOutgoingMessage
from adversarial_actions import QueryFunctionality
from adversarial_actions import InvokeEnvironment

from typing import Dict
from typing import List

n: int = 2
k: int = 2

# Generate protocol parameters
parameter_set = trusted_setup()
protocol_description = protocol_description()

# noinspection PyTypeChecker
parent_parties: List[ParentParty] = [None] * n
# noinspection PyTypeChecker
protocol_party: List[ProtocolParty] = [None] * n
# noinspection PyTypeChecker
ideal_functionalities: List[StandardFunctionality] = [None] * k

# Set up environment and protocol parties
for i, pk, sk in enumerate(parameter_set[:n]):
    parent_parties[i] = ParentParty(pk, sk)
    protocol_party[i] = ProtocolParty(pk, sk, protocol_description[i], k + 1)
environment = Environment(parent_parties)

# Set up ideal functionalities
for i, pk, sk in enumerate(parameter_set[n:n+k]):
    ideal_functionalities[i] = StandardFunctionality(pk, sk)

# Set up the adversary
public_param, private_param = parameter_set[n + k]
adversary = LazyAdversary(public_param, private_param, environment)  # TODO: remove env from the adversary

# Initialise protocol wiring. The first index marks protocol party. The second index marks ideal functionality.
incoming_buffers: Dict[int, Dict[int, LeakyBuffer]] = {i: {j: LeakyBuffer() for j in range(k + 1)} for j in range(n)}
outgoing_buffers: Dict[int, Dict[int, LeakyBuffer]] = {i: {j: LeakyBuffer() for j in range(k + 1)} for j in range(n)}

# Complete execution
action = adversary.next_action(None)
while action is not None:
    if isinstance(action, CorruptParty):
        reply = protocol_party[action.party].corrupt_party()
        action = adversary.next_action(reply)
    elif isinstance(action, ClockIncomingBuffer):
        msg = incoming_buffers[action.target, action.source].clock_message(action.msg_index)
        write_instructions, reply = protocol_party[action.target](action.source, msg)
        for port, msg in write_instructions:
            outgoing_buffers[action.target][port].write_message(msg)
        action = adversary.next_action(reply)
    elif isinstance(action, ClockOutgoingBuffer):
        msg = outgoing_buffers[action.source, action.target].clock_message(action.msg_index)
        if action.target in range(k):
            ideal_functionalities[action.target](action.source, msg)
        else:
            environment(action.source, msg)
        action = adversary.next_action(None)
    elif isinstance(action, SendIncomingMessage):
        write_instructions, reply = protocol_party[action.target].write_to_interpreter(action.source, action.msg)
        for port, msg in write_instructions:
            outgoing_buffers[action.target][port].write_message(msg)
        action = adversary.next_action(reply)
    elif isinstance(action, SendOutgoingMessage):
        write_instructions = protocol_party[action.source].write_to_outgoing_buffer(action.target, action.msg)
        for port, msg in write_instructions:
            outgoing_buffers[action.target][port].write_message(msg)
        action = adversary.next_action(None)
    elif isinstance(action, InvokeEnvironment):
        reply = environment.adversarial_probe(action.msg)
        action = adversary.next_action(reply)
    elif isinstance(action, QueryFunctionality):
        reply = ideal_functionalities[action.target].adversarial_probe(action.module, action.msg)
        action = adversary.next_action(reply)

# Final judgement
print(environment.output)
