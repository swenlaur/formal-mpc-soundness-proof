class InstanceLabel:
    """
    Base class for labelling different protocol instances.
    Instance labels are used inside protocol messages to identify recipient and sender.
    Instance labels are used to index states of interpreters and functionalities.
    """
    pass


class NullInstance(InstanceLabel):
    """
    Special symbol for null-instance used to reference volatile state shared by all instances.
    """
    pass
