from network_components import LocalMemory

from typing import Any
from typing import List


class IOFunctionality:
    """
    Adapter between the environment and stateless interpreters.
    Writes incoming to right memory locations and fetches outputs from memory.
    """
    def __init__(self, public_param: Any, private_param: Any, memory_modules: List[LocalMemory]):
        self.memory_modules: List[LocalMemory] = memory_modules
