from exceptions import EmptyQueueException

class Queue:
  def __init__(self):
    self.data = []
  
  def add(self, x):
    self.data.append(x)
  
  def remove(self):
    if self.empty():
        raise EmptyQueueException()
    x = self.data[0]
    self.data = self.data[1:]
    return x
  
  def empty(self):
    return self.data == []
  
  def __str__(self):
    return str(self.data)
