# Matteo Alessandro Fumis (IN2000249)

from queue import Queue
from exceptions import (
    MemoryExceededException,
    EmptyQueueException,
    IllegalInstructionException,
)


class Lmc:
    """
    Constructor function

    Parameters:
    - Machine code produced by the assembler
    - Optional input values

    The function:
    1. Instantiates fields that characterize the lmc
    2. Copies machine code to memory if it does not exceed memory size
    3. Adds provided input values to input queue
    """
    def __init__(self, machine_code, input_values=None):
        self.memory = [0] * 100
        self.accumulator = 0
        self.program_counter = 0
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.flag = False
        self.halted = False

        if len(machine_code) > 100:
            raise MemoryExceededException(len(machine_code), len(self.memory))
        else:
            for i in range(len(machine_code)):
                self.memory[i] = machine_code[i]

        if input_values:
            for value in input_values:
                self.input_queue.add(value)

    """
    Function run()

    Parameters:
    - A mode of execution, it is a string. 

    The function:
    1. Checks the selected run mode
    2. Executes the program
        - If "standard", executes all the instructions until the halt flag is True
        - If "steps", executes a single instruction and waits for the user input (ENTER) for 
        executing the next
    """
    def run(self, mode):
        match mode:
            case "standard":
                while self.halted is False:
                    self.__execute_instruction()
            case "steps":
                while self.halted is False:
                    self.__execute_instruction()
                    # prints current status at each step
                    print(self)
                    # input() function blocks execution until ENTER pressed
                    input("Press ENTER to continue execution")
        print("Execution ended")

    """
    Function execute_instruction()

    Parameters:
    - None

    The function:
    1. Retrieves the current instruction from the memory address correspondent 
        to the current value of the program counter
    2. Increments the program counter 
    3. Retrieves opcode and operand from the instruction
    4. Depending on the opcode value, executes the correspondent instruction 
        applied to the given operand
    """
    def __execute_instruction(self):
        instruction = self.memory[self.program_counter]
        self.program_counter = self.program_counter + 1

        if self.program_counter >= 100:
            self.halted = True
            raise IllegalInstructionException(
                f"Program counter exceeded memory bounds: {self.program_counter}"
            )

        """
        Integer division by 100 to get the first digit,
        modulus to get the last two digits
        """
        opcode = instruction // 100
        operand = instruction % 100

        # follows the implementation of the instructions
        match opcode:
            case 0:
                self.halted = True
            case 1:
                res = self.accumulator + self.memory[operand]
                if res > 999:
                    self.flag = True
                else:
                    self.flag = False
                self.accumulator = res % 1000

            case 2:
                res = self.accumulator - self.memory[operand]
                if res < 0:
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
                if self.accumulator == 0 and self.flag is False:
                    self.program_counter = operand

            case 8:
                if self.flag is False:
                    self.program_counter = operand

            case 9:
                match operand:
                    case 1:
                        try:
                            self.accumulator = self.input_queue.remove()
                        except EmptyQueueException:
                            self.halted = True
                            self.accumulator = 0
                    case 2:
                        self.output_queue.add(self.accumulator)
                    case _:
                        self.halted = True
                        raise IllegalInstructionException(instruction)

            # default case if none of the previous legal cases is matched
            case _:
                self.halted = True
                raise IllegalInstructionException(instruction)


    #__str()__ dunder method to represent the state of a lmc instance as string
    def __str__(self):
        return (
            f"-------------------------\n"
            f"LMC Status:\n"
            f"  Accumulator: {self.accumulator}\n"
            f"  Program Counter: {self.program_counter}\n"
            f"  Flag: {self.flag}\n"
            f"  Halted: {self.halted}\n"
            f"  Input Queue: {self.input_queue}\n"
            f"  Output Queue: {self.output_queue}\n"
        )
