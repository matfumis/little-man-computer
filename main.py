from assembler import Assembler
from lmc import Lmc

assembler = Assembler()

lines = assembler.get_code_lines('lmc/quine.lmc')
print('Lines: ', lines)

labels, processed_lines = assembler.get_labels(lines)
print('Labels: \n', labels)
print('Processed lines: \n', processed_lines)


memory = assembler.parse_machine_code(labels, processed_lines)
print('Memory: ', memory)


lmc = Lmc(memory, [2, 3, 99])

lmc.run('standard')

print(lmc.output_queue)


