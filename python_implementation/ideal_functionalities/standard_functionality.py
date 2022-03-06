from network_components import InstanceLabel
from network_components import LeakyBuffer

from ideal_functionalities import SharingModule
from ideal_functionalities import ComputationModule
from ideal_functionalities import ReconstructionModule

from typing import Any
from typing import List
from typing import Tuple
from typing import Optional


class StandardFunctionality:
    """
    Ideal functionality is a shell connecting three modules that do the entire work.
    The module writes messages only to outgoing buffers or send them instantly to the adversary.

    To set up the ideal functionality two steps must be carried out:
    * The list of outgoing buffers must be specified.
    * Setup parameters must be passed form the trusted setup.
    """

    def __init__(self, public_param: Any, private_param: Any):
        self.sharing_module: SharingModule = SharingModule(public_param, private_param)
        self.computation_module: ComputationModule = ComputationModule(public_param, private_param)
        self.reconstruction_module: ReconstructionModule = ReconstructionModule(public_param, private_param)

    def set_outgoing_buffers(self, outgoing_buffers: List[LeakyBuffer]):
        """
        To complete the setup one must specify leaky output buffers to protocol parties.
        """
        self.sharing_module.outgoing_buffers = outgoing_buffers

    def __call__(self, input_port: int, msg: Any) -> Optional[Any]:
        """
        Processes inputs from incoming buffers.
        The input is processed by the reconstruction module which can pass data to the computation module.
        The computation module can pass the data to sharing module which writes outcomes to output buffers.

        The reconstruction module and sharing module can also produce outputs for the adversary.
        Then the control goes to the adversary who should give it back to the functionality to complete computation.
        """

        instance, caller, data = self.expand_message(msg)
        abort, data = self.reconstruction_module(input_port, instance, data)
        if abort:
            return data

        abort, data = self.computation_module(instance, data)
        if abort:
            return data

        return self.sharing_module(instance, caller, data)

    def adversarial_probe(self, module: str,  msg: Any) -> Any:
        """
        Adversary can only interact with reconstruction and sharing module.
        The computation module is assumed to be directly inaccessible.
        If needed instructions can be sent through reconstruction module.
        """
        instance, caller, data = self.expand_message(msg)

        if module == 'r':
            abort, data = self.reconstruction_module.adversarial_probe(msg)

            if abort:
                return data

            abort, data = self.computation_module(instance, data)
            if abort:
                return data

            return self.sharing_module(instance, caller, data)

        elif module == 's':
            self.sharing_module.adversarial_probe(instance, caller, data)

    @staticmethod
    def expand_message(msg: Any) -> Tuple[InstanceLabel, InstanceLabel, Any]:
        """
        Splits incoming message into instance, caller, payload tuple.
        """
        pass

