# Matteo Alessandro Fumis (IN2000249)

from exceptions import InvalidFileExtensionException, IllegalInstructionException


class Assembler:
    """
    Constructor function

    Parameters:
    - None

    The function instantiates the field that characterizes the assembler, which is
    the map from all the possible assembly instructions to correspondent opcodes in machine code
    """

    def __init__(self):
        self.instructions = {
            "ADD": 1,
            "SUB": 2,
            "STA": 3,
            "LDA": 5,
            "BRA": 6,
            "BRZ": 7,
            "BRP": 8,
            "INP": 901,
            "OUT": 902,
            "HLT": 0,
            "DAT": None,
        }

    """
    Function assemble()

    Parameters:
    - The path to the source code file

    Returns:
    - A list of instructions in machine code, representing the initial state of lmc memory

    The function:
    1. Extracts 
        - code lines from the source (no extra spaces or comments)
        - a map from label names to correspondent memory addresses
    2. Parses the assembly code and produces the initial memory state
    3. Returns the memory state
    """

    def assemble(self, source_code):
        lines, labels = self.__preprocess_code(source_code)
        memory = self.__parse_code(lines, labels)
        return memory

    """
    Function __preprocess_code()

    Parameters:
    - The path to the source code file

    Returns:
    - A list of instructions
    - A map from each label to the correspondent address

    The function:
    1. Calls __clean_code_lines() to clean up from comments and empty lines
    2. Calls __process_labels() to get 
        - the map of labels
        - code lines without labels declarations
    3. Returns lines and labels map
    """

    def __preprocess_code(self, source_code):
        clean_lines = self.__clean_code_lines(source_code)
        """
        Check for correct extension is put here beacuse, if put before, the exception 
        would be thrown even if the file does not exist
        """
        if not source_code.lower().endswith(".lmc"):
            raise InvalidFileExtensionException(source_code)

        clean_lines, labels = self.__process_labels(clean_lines)

        return clean_lines, labels

    """
    Function __clean_code_lines()

    Parameters:
    - The path to the source code file

    Returns:
    - A list of uppercased code lines with no comments

    The function:
    1. Opens the source code file in read mode
    2. Iterates through the file lines and:
        - if the line contains a comment, keeps the line up
        to the index of the start of the comment, excluded
        - removes spaces from beginning and end of the line
        - if the line is not empty, appends it uppercased to the list
        of line
    3. Closes the file and returns
    """

    def __clean_code_lines(self, source_code):
        file = open(source_code, "r")
        lines = []
        for line in file:
            if "//" in line:
                line = line[: line.index("//")]
            line = line.strip()
            if line:
                lines.append(line.upper())
        file.close()
        return lines

    """
    Function __process_labels()

    Parameters:
    - A list of code lines

    Returns:
    - A map from labels to addresses
    - A list of code lines

    The function:
    1. Instantiates an empty list, an empty map and an address counter
    2. Iterates through the lines
        - Divides the line in tokens
        - If the line has more than 1 token and 
         the first token is not a valid instruction 
         AND it is followed by a valid instruction,
         it means that the first token is a label and 
         adds the first token to the map with the correspondent address
        - Once the label is saved in the map, its declaration
         is removed from the code line
        - At each iteration increments the address counter, in 
        order to keep the correct correspondence between lines and addresses
    3. Returns
    """

    def __process_labels(self, lines):
        processed_lines = []
        labels = {}
        address = 0

        for line in lines:
            tokens = line.split()
            if (
                len(tokens) > 1
                and tokens[0] not in self.instructions
                and tokens[1] in self.instructions
            ):
                labels.update({tokens[0]: address})
                processed_lines.append(" ".join(tokens[1:]))
            else:
                processed_lines.append(line)
            address += 1
        return processed_lines, labels

    """
    Function __parse_code()

    Parameters:
    - A list of code lines
    - A map from labels to addresses

    Returns:
    - Initial memory as list of integers, which are machine code instructions

    The function:
    1. Instantiates an empty list and an address counter
    2. Iterates through the lines to fill the memory content:
        - Divides the line in tokens
        - Checks if the tokens[0] contains a valid instruction
        - if so, sets the opcode depending on the instruction mapping
            - tokens[0] is "DAT": 
                -> directly copies the operand (or label value) in the current address, 0 if no operand
            - tokens[0] is "INP", "OUT" or "HLT":
                -> copies the opcode in the current address (exception if there is token[1])
            - tokens[0] is an other instruction:
                -> tokens[1] is the operand (exception if there is no token[1])
                -> the machine code instruction is computed arithmetically summing the operand 
                to the opcode multiplied by 100
                -> the instruction is copied to the current address
        - Current address value is incremented
    3. Returns
    """

    def __parse_code(self, lines, labels):
        memory = [0] * 100
        address = 0
        for line in lines:
            tokens = line.split()

            if tokens[0] in self.instructions:
                opcode = self.instructions[tokens[0]]

                if tokens[0] == "DAT":
                    if len(tokens) > 1:
                        operand = int(tokens[1])
                        memory[address] = operand
                    else:
                        memory[address] = 0
                elif tokens[0] in ["INP", "OUT", "HLT"]:
                    if len(tokens) > 1:
                        raise IllegalInstructionException(
                            f"Illegal instruction: {tokens[0]} has no operand"
                        )
                    else:
                        memory[address] = opcode
                else:
                    if len(tokens) < 2:
                        raise IllegalInstructionException(
                            f"Illegal instruction: {tokens[0]} has missing operand"
                        )
                    else:
                        if tokens[1] in labels:
                            operand = labels[tokens[1]]
                        else:
                            operand = int(tokens[1])
                        memory[address] = opcode * 100 + operand

                address += 1

            else:
                raise IllegalInstructionException(
                    f"Unknown instruction: {tokens[0]} at code line {address + 1}"
                )

        return memory
