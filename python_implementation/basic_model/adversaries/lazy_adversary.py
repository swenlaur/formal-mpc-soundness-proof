from adversarial_actions import AdversarialAction

from typing import Any


class LazyAdversary:
    """
    Adversary is the master scheduler for the entire collection of machines.
    After the collection is initialised the executions stats from the adversary who choose one adversarial action.
    This triggers computations after which the adversary can explore the outcome and plan a new action.
    Computations continue until the adversary stops after which final judgement is made by the environment.

    The adversary can invoke the following actions
    * corrupt parties
    * invoke environment
    * clock buffers
    * send messages behalf of corrupted parties

    The handle to the environment id the only explicit link to the machines, buffers and ports in the collection.
    The adversary must specify the remaining objects through indices and labels.
    The corresponding knowledge is assumed to be inside the adversarial code.

    The class of lazy adversaries is assumed to satisfy certain restrictions but these are just assumed to be
    fulfilled and not forced by the code structure.
    """

    def __init__(self, public_param: Any, private_param: Any):
        self.public_param: Any = public_param
        self.private_param: Any = private_param

    def next_action(self, arg: Any) -> AdversarialAction:
        pass
