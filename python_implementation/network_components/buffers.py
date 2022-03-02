from network_components import InputPort
from network_components import OutputPort

from typing import Any
from typing import List
from typing import Tuple
from typing import Callable


class Buffer:
    """In our model all buffers are clocked by the adversary."""

    def __init__(self, input_port: InputPort, output_port: OutputPort):
        self.input_port: InputPort = input_port
        self.output_port: OutputPort = output_port
        self.messages: List[Any] = []

    def clock_message(self, n: int) -> Tuple[OutputPort, Any]:
        assert 0 <= n < len(self.messages)
        msg = self.messages.pop(n)
        return self.output_port, msg


class LeakyBuffer(Buffer):
    """Abstract leak function allows user to specify arbitrary leak models."""
    def __init__(self):
        super().__init__()
        self.leak_function: Callable[[Any], Any] = None

    def peek_message_tag(self, n: int) -> Any:
        assert self.leak_function
        assert 0 <= n < len(self.messages)
        return self.leak_function(self.messages[n])
