class Queue:
  def __init__(self):
    self.data = []
  
  def add(self, x):
    """Add an element to the end of the queue"""
    self.data.append(x)
  
  def remove(self):
    """Remove and return the first element from the queue.
    Raises Exception if queue is empty."""
    if self.empty():
        raise Exception("Input queue is empty")
    x = self.data[0]
    self.data = self.data[1:]
    return x
  
  def empty(self):
    """Check if the queue is empty."""
    return len(self.data) == 0
  
  def __str__(self):
    """String representation of the queue"""
    return str(self.data)


'''
class Queue:
  def __init__(self):
    self.data = []

  def add(self, x):
    self.data.append(x)

  def remove(self):
    if self.data == []:
      raise Exception()
    x = self.data[0]
    self.data = self.data[1:]
    return x

    def empty(self):
        return self.data == []

'''