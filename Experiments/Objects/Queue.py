# TODO - More queues!!!
class FIFOQueue:
    """Implementation of a simple FIFO queue."""
    queue: list
    def __init__(self):
        """The constructor for the queue."""
        self.queue = []

    def pop(self):
        """Pops off 😎 from the queue."""
        if (len(self.queue) <= 0):
            return None
        return self.queue.pop(0)
    
    def push(self, obj):
        """Pushes onto the queue."""
        self.queue.append(obj)

    def clear(self):
        """Clears the queue."""
        self.queue = []

    def peak(self):
        """Peak at the next value in the queue."""
        if (len(self.queue) <= 0):
            return None
        return self.queue[0]
    
    def length(self) -> int:
        """Returns the length of the queue.

        Returns:
            int: The length of the queue
        """
        return len(self.queue)