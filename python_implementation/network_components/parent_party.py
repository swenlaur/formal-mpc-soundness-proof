from .machine import Machine

from typing import Any


class ParentParty(Machine):
    """
    Empty base class for all adversarial adapters.
    """

    def __init__(self, public_param: Any, private_param: Any):
        self.public_param: Any = public_param
        self.private_param: Any = private_param
