# Matteo Alessandro Fumis (IN2000249)

from queue import Queue
from exceptions import MemoryExceededException, EmptyQueueException, IllegalInstructionException

class Lmc:

  def __init__(self, binary, input_values=None):
    self.memory = [0] * 100 
    self.accumulator = 0  
    self.program_counter = 0  
    self.flag = False  
    self.input_queue = Queue()  
    self.output_queue = Queue()  
    self.halted = False  

    if len(binary) > 100:
      raise MemoryExceededException(len(binary), len(self.memory))
    else:
      for i in range(len(binary)):
        self.memory[i] = binary[i]

    if input_values:
      for value in input_values:
        self.input_queue.add(value)

  def run(self, mode):
      match mode: 
        case 'standard':
          while self.halted is False:
              self.__execute_instruction()
        case 'steps':
          while self.halted is False:
              opcode, operand = self.__execute_instruction()
              print(self)
              input("Press ENTER to continue execution")
      print('Execution ended')
  

  def __execute_instruction(self):
    instruction = self.memory[self.program_counter]
    self.program_counter = (self.program_counter + 1) % 1000

    opcode = instruction // 100
    operand = instruction % 100

    match opcode:
      case 0: 
        self.halted = True
        return opcode, operand

      case 1: 
        res = self.accumulator + self.memory[operand] 
        if(res > 999):
          self.flag = True
        else:
          self.flag = False
        self.accumulator = res % 1000

      case 2:
        res = self.accumulator - self.memory[operand]
        if(res < 0):
          self.flag = True
        else:
          self.flag = False
        self.accumulator = res % 1000

      case 3: 
        self.memory[operand] = self.accumulator

      case 5:
        self.accumulator = self.memory[operand]

      case 6:
        self.program_counter = operand

      case 7: 
        if(self.accumulator == 0 and self.flag is False):
          self.program_counter = operand

      case 8:
        if(self.flag is False):
          self.program_counter = operand

      case 9: 
        match operand:
          case 1: 
            try:
              self.accumulator = self.input_queue.remove() 
            except EmptyQueueException():
              self.halted = True
              self.accumulator = 0 
          case 2: 
            self.output_queue.add(self.accumulator)
          case _:
            self.halted = True
            raise IllegalInstructionException(instruction)

      case _:  
        self.halted = True
        raise IllegalInstructionException(instruction)

    return opcode, operand    


  def __str__(self):
    status = '-------------------------\n'
    status += "LMC Status:\n"
    status += f"  Accumulator: {self.accumulator}\n"
    status += f"  Program Counter: {self.program_counter}\n"
    status += f"  Flag: {self.flag}\n"
    status += f"  Halted: {self.halted}\n"
    status += f"  Input Queue: {self.input_queue}\n"
    status += f"  Output Queue: {self.output_queue}\n"

    return status