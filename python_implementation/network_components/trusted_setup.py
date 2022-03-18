from typing import Any
from typing import List
from typing import Tuple


def trusted_setup() -> List[Tuple[Any, Any]]:
    """
    Probabilistic generation of public and private setup parameters for all parties including adversary.
    In the original model the trusted setup is machine but here we implement it as a stateless function.

    The size of the output is n + k + 1 where n is the number of parties and k is the number of ideal functionalities.
    """
    pass
