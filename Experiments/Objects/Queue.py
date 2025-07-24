class FIFOQueue:
    queue: list
    def __init__(self):
        self.queue = []

    def pop(self):
        if (len(self.queue) <= 0):
            return None
        return self.queue.pop(0)
    
    def push(self, obj):
        self.queue.append(obj)

    def clear(self):
        self.queue = []

    def peak(self):
        if (len(self.queue) <= 0):
            return None
        return self.queue[0]
    
    def length(self):
        return len(self.queue)