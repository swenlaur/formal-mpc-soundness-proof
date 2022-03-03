from shared_components import Environment
from shared_components import TrustedSetup
from shared_components import ParentParty
from shared_components import ProtocolDescription

from basic_model import StatefulInterpreter
from basic_model import CorruptionModule
from basic_model import StandardFunctionality
from basic_model import LazyAdversary
from basic_model import CorruptionModule

from network_components import LeakyBuffer
from network_components import Machine
from network_components import InputPort
from network_components import OutputPort

from typing import Dict
from typing import Tuple
from typing import List

n = 2
k = 2

# Generate protocol parameters
f_setup = TrustedSetup(n, k)
parameter_set = f_setup.generate_parameters()
protocol_description = ProtocolDescription()

# Set up environment
parent_parties = [None] * n
for i, pk, sk in enumerate(parameter_set[:n]):
    parent_parties[i] = ParentParty(pk, sk)
environment = Environment(parent_parties)

# Initialise protocol parties
interpreters: List[StatefulInterpreter] = [None] * n
corruption_modules: List[CorruptionModule] = [None] * n
for i, pk, sk in enumerate(parameter_set[:n]):
    interpreters[i] = StatefulInterpreter(pk, sk, protocol_description[i])
    corruption_modules[i] = CorruptionModule(interpreters[i])

ideal_functionalities: List[StandardFunctionality] = [None] * k
for i, pk, sk in enumerate(parameter_set[n:n+k]):
    ideal_functionalities[i] = StandardFunctionality(pk, sk)

# Initialise protocol wiring. Buffers are named from the perspective of parties
# As there is exactly one buffer bar between machines we can use machines to index buffers
incoming_buffers: Dict[Tuple[Machine, Machine], LeakyBuffer] = {}
outgoing_buffers: Dict[Tuple[Machine, Machine], LeakyBuffer] = {}
for i, p in enumerate(interpreters):
    for f in ideal_functionalities + [environment]:
        incoming_buffers[p, f] = LeakyBuffer(InputPort(f, i), OutputPort(p, i))
        outgoing_buffers[p, f] = LeakyBuffer(InputPort(p, i), OutputPort(f, i))

# Set up the adversary
pk, sk = parameter_set[n + k]
adversary = LazyAdversary(pk, sk, environment, interpreters, ideal_functionalities, incoming_buffers, outgoing_buffers)
target_machine, port, msg = adversary.ping()

while target_machine is not None:
    target_machine, port, msg = target_machine(port, msg)
    if target_machine is None:
        target_machine, port, msg = adversary.ping()

# adversary clock buffer and calls the corruption module with output


print(environment.output)
