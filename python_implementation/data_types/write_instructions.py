from typing import Any
from typing import List
from typing import Tuple

# WriteInstruction is in the form [(port, msg), ..., (port, msg)]
WriteInstructions = List[Tuple[int, Any]]
