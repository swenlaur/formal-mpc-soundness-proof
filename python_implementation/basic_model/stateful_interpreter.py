from state_components import ThreadState

from typing import Any
from typing import List
from typing import Tuple
from typing import Optional


class StatefulInterpreter:
    """
    Interpreter can use public and private parameters to interpret code.
    The code will be a protocol specific but it can be set only once.
    The interpreter can execute several protocol instances with separate states.
    Interpreter will be controlled by the corruption module who invokes it and patches its output
    """

    def __init__(self, public_param: Any, private_param: Any, code: Any):
        self.public_param: Any = public_param
        self.private_param: Any = private_param

        self.code = code
        self.state: List[Tuple[ThreadState, int]] = []

    def __call__(self, input_port: int, msg: Any) -> Optional[Tuple[int, Any]]:
        """
        Returns a port label and a corresponding message or nothing.
        This function should be called by the corruption module.
        """
        instance: Any
        pass
