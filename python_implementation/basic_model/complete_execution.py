from shared_components import Environment
from shared_components import TrustedSetup
from shared_components import ParentParty
from shared_components import ProtocolDescription

from basic_model import StatefulInterpreter
from basic_model import StandardFunctionality
from basic_model import LazyAdversary

from typing import Dict
from typing import Any

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
protocol_parties = [None] * n
for i, pk, sk in enumerate(parameter_set[:n]):
    protocol_parties[i] = StatefulInterpreter(pk, sk, protocol_description[i])

ideal_functionalities = [None] * k
for i, pk, sk in enumerate(parameter_set[n:n+k]):
    ideal_functionalities[i] = StandardFunctionality(pk, sk)

# Initialise protocol wiring
input_buffers: Dict[Any, Any]
output_buffers: Dict[Any, Any]
input_buffers = {(p, i): None for p in protocol_parties for i in ideal_functionalities + [environment]}
output_buffers = {(p, i): None for p in protocol_parties for i in ideal_functionalities + [environment]}

# Connect buffers
for party in protocol_parties:
    party.connect_buffers(input_buffers=None, output_buffers=None)

for funct in ideal_functionalities:
    funct.connect_buffers(input_buffers=None, output_buffers=None)

environment.connect_buffers(input_buffers=None, output_buffers=None)

# Set up the adversary
pk, sk = parameter_set[n + k]
adversary = LazyAdversary(pk, sk, environment, protocol_parties, ideal_functionalities, input_buffers, output_buffers)
target_machine, port, msg = adversary.ping()

while target_machine is not None:
    target_machine, port, msg = target_machine(port, msg)
    if target_machine is None:
        target_machine, port, msg = adversary.ping()

print(environment.output)
