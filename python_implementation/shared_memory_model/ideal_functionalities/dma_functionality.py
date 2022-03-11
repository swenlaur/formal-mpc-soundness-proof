from network_components import LeakyBuffer
from network_components import LocalMemory

from typing import Any
from typing import List


class DMAFunctionality:
    """
    Ideal functionality that uses shared memory modules to fetch and dispatch data.
    TODO: Update documentation
    Ideal functionality is a shell connecting three modules that do the entire work.
    The module writes messages only to outgoing buffers or send them instantly to the adversary.

    To set up the ideal functionality two steps must be carried out:
    * The list of outgoing buffers must be specified.
    * Setup parameters must be passed form the trusted setup.
    """
    def __init__(self, public_param: Any, private_param: Any, memory_modules: List[LocalMemory]):
        self.memory_modules: List[LocalMemory] = memory_modules

    def set_outgoing_buffers(self, outgoing_buffers: List[LeakyBuffer]):
        """
        To complete the setup one must specify leaky output buffers to protocol parties.
        """
        self.sharing_module.outgoing_buffers = outgoing_buffers
