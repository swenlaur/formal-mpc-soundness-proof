from network_components import Machine

from typing import Any
from typing import List


class Environment(Machine):

    def __init__(self, parent_parties: List[Machine]):
        pass

    def adversarial_probe(self, msg: Any) -> Any:
        pass

    @property
    def output(self):
        pass


