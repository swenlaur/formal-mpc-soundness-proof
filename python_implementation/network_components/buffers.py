from typing import Any
from typing import List


class Buffer:
    """
    The class does not explicitly specify who clocks buffers.
    The latter will be implicitly determined by the remaining code.
    The one who calls clock_message(...) function is the clocker.
    The one who calls write_message(...) function is the sender.
    For most buffers the clocker is the adversary.
    """

    def __init__(self):
        self.messages: List[Any] = []

    def write_message(self, msg: Any) -> None:
        self.messages.append(msg)

    def clock_message(self, n: int) -> Any:
        assert 0 <= n < len(self.messages)
        return self.messages.pop(n)


class LeakyBuffer(Buffer):
    """
    Abstract leak function allows user to specify arbitrary leak models.
    In our model, the buffer leaks the first component of the message by default.
    The one who calls peek_message(...) and clock_message(...) functions is the clocker.
    This has to be a single machine.
    """
    def __init__(self):
        super().__init__()

    def peek_message(self, n: int) -> Any:
        assert self.leak_function
        assert 0 <= n < len(self.messages)
        return self.leak_function(self.messages[n])

    @staticmethod
    def leak_function(msg: Any) -> Any:
        return msg[0]
