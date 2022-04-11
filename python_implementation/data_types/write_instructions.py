from typing import Any
from typing import List
from typing import Tuple

from .labels import FunctId

# WriteInstruction is in the form [(port, msg), ..., (port, msg)]
WriteInstructions = List[Tuple[FunctId, Any]]
