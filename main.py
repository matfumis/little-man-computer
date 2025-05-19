from assembler import Assembler
from lmc import Lmc

filename = 'lmc/exec.lmc'

assembler = Assembler()
memory = assembler.compile(filename)

lmc = Lmc(memory, [901, 902, 705, 600, 0, 4, 5, 6, 7, 8, 9, 0])

lmc.run('standard')

print(lmc.output_queue)


