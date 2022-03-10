class MemoryLocation:
    """
    Address of a memory location.
    Usually an integer or a tuple integers.
    Different machines can use different types of memory locations.
    """
    pass


class PinnedLocation(MemoryLocation):
    """
    Default address for memory segment with single entry.
    """
    pass
