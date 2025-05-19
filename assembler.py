class Assembler:
  def __init__(self):
      self.instructions = {
          'ADD': 1,  
          'SUB': 2,   
          'STA': 3,   
          'LDA': 5,   
          'BRA': 6,  
          'BRZ': 7,  
          'BRP': 8,   
          'INP': 901, 
          'OUT': 902, 
          'HLT': 0,  
          'DAT': None 
      }

  def compile(self, filename):
    labels, lines = self.__preprocess_code(filename)
    memory = self.__parse_machine_code(lines, labels)
    return memory

  def __preprocess_code(self, filename):
    clean_lines = self.__get_code_lines(filename)
    labels = self.__get_labels(clean_lines)
    clean_lines = self.__remove_labels(clean_lines, labels)

    return clean_lines, labels

  def __get_code_lines(self, filename):
    file = open(filename, 'r')
    lines = []
    try:
      for line in file:
        if '//' in line:
          line = line[:line.index('//')]
        line = line.strip()
        if line:
          lines.append(line.upper())

    finally:
      file.close()
    return lines


  def __get_labels(self, lines):
    labels = {}
    address = 0

    for line in lines:
      tokens = line.split()
      if len(tokens)>1 and tokens[0] not in self.instructions and tokens[0] not in labels :
        labels.update({tokens[0]: address})
        address+=1
      else:
        address+=1
    return labels

  def __remove_labels(self, lines, labels):
    processed_lines = []
    for line in lines:
      tokens = line.split()
      if len(tokens) > 1 and tokens[0] in labels:
        processed_lines.append(' '.join(tokens[1:]))
      else:
        processed_lines.append(line)
    return processed_lines

  def __parse_machine_code(self, labels, lines):
    memory = [0] * 100
    address = 0
    
    for line in lines:
        tokens = line.split()
        tokens = [token.upper() for token in tokens]       

        if tokens[0] in self.instructions:
            opcode = self.instructions[tokens[0]]
            
            if tokens[0] == 'DAT':
                if len(tokens) > 1:
                    if tokens[1] in labels:
                        operand = labels[tokens[1]]
                    else:    
                        operand = int(tokens[1])
                    memory[address] = operand
                else:
                    memory[address] = 0
            else:

                if len(tokens) == 1:
                    memory[address] = opcode
                elif len(tokens) > 1:
                    if tokens[1] in labels:
                        operand = labels[tokens[1]]
                    else:    
                        operand = int(tokens[1])
                    memory[address] = opcode * 100 + operand
                    
            address += 1
    return memory

    
    


    