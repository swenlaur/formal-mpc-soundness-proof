from network_components import InputPort
from network_components import OutputPort

from typing import Any
from typing import List
from typing import Tuple
from typing import Callable


class Buffer:
    """
    The class does not explicitly specify who clocks buffers.
    The latter will be implicitly determined by the remaining code.
    The one who calls clock_message(...) function is the clocker.
    The one who calls write_message(...) function is the sender.
    For most buffers the clocker is the adversary.
    """

    def __init__(self, input_port: InputPort, output_port: OutputPort):
        self.input_port: InputPort = input_port
        self.output_port: OutputPort = output_port
        self.messages: List[Any] = []

    def write_message(self, msg: Any) -> None:
        self.messages.append(msg)

    def clock_message(self, n: int) -> Tuple[OutputPort, Any]:
        assert 0 <= n < len(self.messages)
        msg = self.messages.pop(n)
        return self.output_port, msg


class LeakyBuffer(Buffer):
    """
    Abstract leak function allows user to specify arbitrary leak models.
    In our model, the buffer leaks the first component of the message by default.
    The one who calls peek_message(...) and clock_message(...) functions is the clocker.
    This has to be a single machine.
    """

    leak_function: Callable[[Tuple[Any, Any]], Any] = lambda msg: msg[0]

    def __init__(self, input_port: InputPort, output_port: OutputPort):
        super().__init__(input_port, output_port)

    def peek_message(self, n: int) -> Any:
        assert self.leak_function
        assert 0 <= n < len(self.messages)
        return self.leak_function(self.messages[n])
