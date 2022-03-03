from network_components import Buffer
from typing import List


class Machine:
    def __init__(self):
        self.outgoing_buffers: List[Buffer] = []

