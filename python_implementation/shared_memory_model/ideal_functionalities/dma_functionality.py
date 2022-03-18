from data_types import InstanceLabel
from network_components import LocalMemory

from typing import Any
from typing import List
from typing import Tuple
from typing import Optional


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
        self.reconstruction_module = None
        self.sharing_module = None
        self.computation_module = None

    def __call__(self, input_port: int, msg: Any) -> Optional[Any]:
        pass

    def adversarial_probe(self, module: str,  msg: Any) -> Any:
        """
        Adversary can only interact with reconstruction and sharing module.
        The computation module is assumed to be directly inaccessible.
        If needed instructions can be sent through reconstruction module.
        """
        instance, caller, data = self.expand_message(msg)

        if module == 'r':
            abort, data = self.reconstruction_module.adversarial_probe(instance, msg)

            if abort:
                return data

            abort, data = self.computation_module(instance, data)
            if abort:
                return data

            return self.sharing_module(instance, caller, data)

        elif module == 's':
            self.sharing_module.adversarial_probe(instance, caller, data)

    def expand_message(self, msg: Any) -> Tuple[InstanceLabel, InstanceLabel, Any]:
        pass
