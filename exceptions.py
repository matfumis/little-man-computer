class MemoryExceededException(Exception):
  def __init__(self, binary_size, memory_size, message=None):
    self.binary_size = binary_size
    self.memory_size = memory_size
    if not message:
      self.message = f'Binary program size ({binary_size}) exceeds available LMC memory ({memory_size})'
    super().__init__(self.message) 

class EmptyQueueException(Exception):
  def __init__(self, message=None):
    if not message:
      self.message = 'Queue aldready empty'
    super().__init__(self.message) 

class IllegalInstructionException(Exception):
  def __init__(self, instruction, message=None):
    if not message:
      self.message = f'Invalid instruction: {instruction}'
    super().__init__(self.message) 

class InvalidFileExtensionException(Exception):
  def __init__(self, filename, message=None):
    if not message:
      self.message = f'Invalid file extension for {filename} Expected .lmc extension.'
    super().__init__(self.message)
