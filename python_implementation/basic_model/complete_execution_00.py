from data_types import ProtocolDescription

from basic_model import StatefulInterpreter
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
from typing import Tuple
from typing import List

n: int = 2
k: int = 2

# Generate protocol parameters
parameter_set = trusted_setup()
protocol_description = ProtocolDescription()

# Set up environment
# noinspection PyTypeChecker
parent_parties: List[ParentParty] = [None] * n
for i, pk, sk in enumerate(parameter_set[:n]):
    parent_parties[i] = ParentParty(pk, sk)
environment = Environment(parent_parties)

# Initialise protocol parties
# noinspection PyTypeChecker
interpreters: List[StatefulInterpreter] = [None] * n
# noinspection PyTypeChecker
corruption_modules: List[ProtocolParty] = [None] * n
for i, pk, sk in enumerate(parameter_set[:n]):
    corruption_modules[i] = ProtocolParty(pk, sk, protocol_description[i], k + 1)

# noinspection PyTypeChecker
ideal_functionalities: List[StandardFunctionality] = [None] * k
for i, pk, sk in enumerate(parameter_set[n:n+k]):
    ideal_functionalities[i] = StandardFunctionality(pk, sk)

# Initialise protocol wiring. Buffers are indexed with integers for universality
incoming_buffers: Dict[Tuple[int, int], LeakyBuffer] = {}
outgoing_buffers: Dict[Tuple[int, int], LeakyBuffer] = {}
for i, p in enumerate(interpreters):
    # noinspection PyTypeChecker
    for j, f in enumerate(ideal_functionalities + [environment]):
        incoming_buffers[i, j] = LeakyBuffer()
        outgoing_buffers[i, j] = LeakyBuffer()

# Complete setup by specifying outgoing buffers
for i, corruption_module in enumerate(corruption_modules):
    corruption_module.set_outgoing_buffers([outgoing_buffers[i, j] for j in range(k + 1)])
for j, functionality in enumerate(ideal_functionalities):
    functionality.set_outgoing_buffers([incoming_buffers[i, j] for i in range(n)])
environment.set_outgoing_buffers([incoming_buffers[i, k+1] for i in range(n)])

# Set up the adversary
public_param, private_param = parameter_set[n + k]
adversary = LazyAdversary(public_param, private_param, environment)

# Complete execution
action = adversary.next_action(None)
while action is not None:
    if isinstance(action, CorruptParty):
        reply = corruption_modules[action.party].corrupt_party()
        action = adversary.next_action(reply)
    elif isinstance(action, ClockIncomingBuffer):
        msg = incoming_buffers[action.target, action.source].clock_message(action.msg_index)
        reply = corruption_modules[action.target](action.source, msg)
        action = adversary.next_action(reply)
    elif isinstance(action, ClockOutgoingBuffer):
        msg = outgoing_buffers[action.source, action.target].clock_message(action.msg_index)
        if action.target in range(k):
            ideal_functionalities[action.target](action.source, msg)
        else:
            environment(action.source, msg)
        action = adversary.next_action(None)
    elif isinstance(action, SendIncomingMessage):
        reply = corruption_modules[action.target].write_to_interpreter(action.source, action.msg)
        action = adversary.next_action(reply)
    elif isinstance(action, SendOutgoingMessage):
        corruption_modules[action.source].write_to_outgoing_buffer(action.target, action.msg)
        action = adversary.next_action(None)
    elif isinstance(action, InvokeEnvironment):
        reply = environment.adversarial_probe(action.msg)
        action = adversary.next_action(reply)
    elif isinstance(action, QueryFunctionality):
        reply = ideal_functionalities[action.target].adversarial_probe(action.module, action.msg)
        action = adversary.next_action(reply)

# Final judgement
print(environment.output)
