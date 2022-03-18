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
incoming_buffers: Dict[int, Dict[int, LeakyBuffer]] = {i: {j: LeakyBuffer() for j in range(k + 1)} for i in range(n)}
outgoing_buffers: Dict[int, Dict[int, LeakyBuffer]] = {i: {j: LeakyBuffer() for j in range(k + 1)} for i in range(n)}

# Complete execution
action = adversary.next_action(None)
while action is not None:
    if isinstance(action, CorruptParty):
        reply = protocol_parties[action.party].corrupt_party()
        action = adversary.next_action(reply)
    elif isinstance(action, ClockIncomingBuffer) and not protocol_parties[action.target].corrupted:
        msg = incoming_buffers[action.target][action.source].clock_message(action.msg_index)
        protocol_parties[action.target](action.source, msg)
        action = adversary.next_action(None)
    elif isinstance(action, ClockIncomingBuffer) and protocol_parties[action.target].corrupted:
        msg = incoming_buffers[action.target][action.source].clock_message(action.msg_index)
        protocol_parties[action.target](action.source, msg)
        reply = protocol_parties[action.target].write_to_interpreter(action.source, msg)
        action = adversary.next_action((action.source, msg))
        assert isinstance(action, SendIncomingMessage)
        action = adversary.next_action(reply)
    elif isinstance(action, ClockOutgoingBuffer):
        msg = outgoing_buffers[action.source][action.target].clock_message(action.msg_index)
        if action.target in range(k):
            ideal_functionalities[action.target](action.source, msg)
        else:
            environment(action.source, msg)
        action = adversary.next_action(None)
    elif isinstance(action, SendOutgoingMessage):
        protocol_parties[action.source].write_to_outgoing_buffer(action.target, action.msg)
        action = adversary.next_action(None)
    elif isinstance(action, InvokeEnvironment):
        reply = environment.adversarial_probe(action.msg)
        action = adversary.next_action(reply)
    elif isinstance(action, QueryFunctionality):
        reply = ideal_functionalities[action.target].adversarial_probe(action.module, action.msg)
        action = adversary.next_action(reply)

# Final judgement
print(environment.output)
