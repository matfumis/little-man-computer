# Matteo Alessandro Fumis (IN2000249)

from exceptions import InvalidFileExtensionException, IllegalInstructionException


class Assembler:
    """
    Constructor function

    Prameters:
    - None

    The function instantiates the field that characterize the assembler, which is
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

    Prameters:
    - The path to the source code file

    Returns:
    - A list of instructions in machine code, representing the initial state of 
        lmc memory

    The function:
    1. Extracts 
        - code lines from the source (no extra spaces or comments)
        - a map from lable names to correspondent memory addresses
    2. Parses the assembly code to machine code
    3. Returns
    """

    def assemble(self, source_code):
        lines, labels = self.__preprocess_code(source_code)
        machine_code = self.__parse_machine_code(lines, labels)
        return machine_code

    """
    Function __preprocess_code()

    Parameters:
    - The path to the source code file

    Returns:
    - A list of instructions
    - A map, mapping each label to the correspondent address

    The function:
    1. Calls __clean_code_lines() to clean up from comments and empty lines
    2. Calls __process_labels() to get 
        - the map of labels
        - code lines without labels declarations
    3. Returns
    """

    def __preprocess_code(self, source_code):
        clean_lines = self.__clean_code_lines(source_code)
        """
        Check for correct extension put here beacuse, if put before, the exception 
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
        - if the line is not empty, appends it upercased to the list
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
         and it is followed by a valid instruction,
         adds it to the map with the correspondent address
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
            if len(tokens) > 1 and tokens[0] not in self.instructions and tokens[1] in self.instructions:
                labels.update({tokens[0]: address})
                processed_lines.append(" ".join(tokens[1:]))
            else:
                processed_lines.append(line)
            address += 1
        return processed_lines, labels

    """
    Function __parse_machine_code()

    Parameters:
    - A list of code lines
    - A map from labels to addresses

    Returns:
    - A list of integers (machine code)

    The function:
    1. Instantiates an empty list and an address counter
    2. Iterates through the lines:
        - Divides the line in tokens
        - Checks if the first token containes a valid instruction
        - if, so:
            - checks if the instrucion 
    """

    def __parse_machine_code(self, lines, labels):
        machine_code = [0] * 100
        address = 0

        for line in lines:
            tokens = line.split()

            if tokens[0] in self.instructions:
                opcode = self.instructions[tokens[0]]

                if tokens[0] == "DAT":
                    if len(tokens) > 1:
                        if tokens[1] in labels:
                            operand = labels[tokens[1]]
                        else:
                            operand = int(tokens[1])
                        machine_code[address] = operand
                    else:
                        machine_code[address] = 0
                else:
                    if len(tokens) == 1:
                        machine_code[address] = opcode
                    elif len(tokens) > 1:
                        if tokens[1] in labels:
                            operand = labels[tokens[1]]
                        else:
                            operand = int(tokens[1])
                        machine_code[address] = opcode * 100 + operand

                address += 1
            
            else:
                raise IllegalInstructionException(f"Unknown instruction: {tokens[0]} at line {address}")
                
        return machine_code

