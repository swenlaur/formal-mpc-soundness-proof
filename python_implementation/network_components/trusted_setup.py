from typing import Any
from typing import List
from typing import Tuple


class TrustedSetup:
    """
    Empty base class for all environments.
    """

    def __init__(self, n: int, k: int):
        self.output_size = n + k + 1

    def __call__(self) -> List[Tuple[Any, Any]]:
        pass
