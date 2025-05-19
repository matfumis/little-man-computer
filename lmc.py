# Matteo Alessandro Fumis (IN2000249)

from queue import Queue

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
      raise Exception('Not enough memory for selected program')
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
              print(f"Performed operation = {opcode}, operand {operand}")
              input("Press ENTER to continue execution")
      print('Execution ended')
  

  def __execute_instruction(self):
    instruction = self.memory[self.program_counter]
    self.program_counter = (self.program_counter + 1) % 100

    opcode = instruction // 100
    operand = instruction % 100

    match opcode:
      case 0: 
        self.halted = True
        return opcode, operand

      case 1: 
        res = self.accumulator + self.memory[operand] 
        if(res >= 1000):
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
            if self.input_queue.empty():
                print("Input queue is empty - halting program")
                self.halted = True
                self.accumulator = 0
            else:
                self.accumulator = self.input_queue.remove() 
          case 2: 
            self.output_queue.add(self.accumulator)
          case _:
            self.halted = True
            raise Exception(f"Invalid I/O instruction: {instruction}")

      case _:  
        self.halted = True
        raise Exception(f"Invalid instruction: {instruction}")

    return opcode, operand    