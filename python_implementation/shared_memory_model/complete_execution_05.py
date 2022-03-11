from data_types import ProtocolDescription
from network_components import Environment
from network_components import TrustedSetup
from network_components import ParentParty

from basic_model import LazyAdversary
from shared_memory_model import StatelessInterpreter
from shared_memory_model import DMAFunctionality
from shared_memory_model import DummyAdversarialAdapter

from network_components import LeakyBuffer
from network_components import InputPort
from network_components import OutputPort
from network_components import LocalMemory


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

n = 2
k = 2

# Generate protocol parameters
f_setup = TrustedSetup(n, k)
parameter_set = f_setup()
protocol_description = ProtocolDescription()

# Set up environment
# noinspection PyTypeChecker
parent_parties: List[ParentParty] = [None] * n
for i, pk, sk in enumerate(parameter_set[:n]):
    parent_parties[i] = ParentParty(pk, sk)
environment = Environment(parent_parties)

# Initialise protocol parties
# noinspection PyTypeChecker
interpreters: List[StatelessInterpreter] = [None] * n
# noinspection PyTypeChecker
memory_modules: List[LocalMemory] = [None] * n
# noinspection PyTypeChecker
adversarial_adapters: List[DummyAdversarialAdapter] = [None] * n
for i, pk, sk in enumerate(parameter_set[:n]):
    memory_modules[i] = LocalMemory()
    interpreters[i] = StatelessInterpreter(pk, sk, protocol_description[i], k + 1, memory_modules[i])
    adversarial_adapters[i] = DummyAdversarialAdapter(memory_modules[i])

# noinspection PyTypeChecker
ideal_functionalities: List[DMAFunctionality] = [None] * k
for i, pk, sk in enumerate(parameter_set[n:n+k]):
    ideal_functionalities[i] = DMAFunctionality(pk, sk, memory_modules)

# Initialise protocol wiring. Buffers are indexed with integers for universality
incoming_buffers: Dict[Tuple[int, int], LeakyBuffer] = {}
outgoing_buffers: Dict[Tuple[int, int], LeakyBuffer] = {}

for i, p in enumerate(interpreters):
    # noinspection PyTypeChecker
    for j, f in enumerate(ideal_functionalities + [environment]):
        incoming_buffers[i, j] = LeakyBuffer(InputPort(f, i), OutputPort(p, i))
        outgoing_buffers[i, j] = LeakyBuffer(InputPort(p, i), OutputPort(f, i))

# Complete setup by specifying outgoing buffers
for i, interpreter in enumerate(interpreters):
    interpreter.set_outgoing_buffers([outgoing_buffers[i, j] for j in range(k + 1)])
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
        reply = adversarial_adapters[action.party].corrupt_party()
        action = adversary.next_action(reply)
    elif isinstance(action, ClockIncomingBuffer) and not memory_modules[action.target].corrupted:
        msg = incoming_buffers[action.target, action.source].clock_message(action.msg_index)
        interpreters[action.target](action.source, msg)
        reply = adversarial_adapters[action.target].clock_incoming_buffer(action.source, action.msg_index)
        action = adversary.next_action(reply)
    elif isinstance(action, ClockIncomingBuffer) and memory_modules[action.target].corrupted:
        msg = incoming_buffers[action.target, action.source].clock_message(action.msg_index)
        interpreters[action.target](action.source, msg)
        adversarial_adapters[action.target].clock_incoming_buffer(action.source, action.msg_index)
        adversary.next_action((action.source, msg))
        reply = adversarial_adapters[action.target].write_to_interpreter(action.source, action.msg)
        action = adversary.next_action(reply)
    elif isinstance(action, ClockOutgoingBuffer):
        adversarial_adapters[action.source].clock_outgoing_buffer(action.target, action.msg_index)
        msg = outgoing_buffers[action.source, action.target].clock_message(action.msg_index)
        if action.target in range(k):
            ideal_functionalities[action.target](action.source, msg)
        else:
            environment(action.source, msg)
        action = adversary.next_action(None)
    elif isinstance(action, SendOutgoingMessage):
        adversarial_adapters[action.source].write_to_outgoing_buffer(action.target, action.msg)
        action = adversary.next_action(None)
    elif isinstance(action, InvokeEnvironment):
        reply = environment.adversarial_probe(action.msg)
        action = adversary.next_action(reply)
    elif isinstance(action, QueryFunctionality):
        reply = ideal_functionalities[action.target].adversarial_probe(action.module, action.msg)
        action = adversary.next_action(reply)

# Final judgement
print(environment.output)
