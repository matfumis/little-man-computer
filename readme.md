# Little Man Computer (LMC)

---
## Overview

This project consists in the implementation in Python of the Little Man 
Computer. The program takes as input a `.lmc` source file, compiles it and executes it
with a single command from command line.   
The execution can be:
- **standard**: the execution of the compiled program 
is made all at once and the user gets the just output when completed
- by **steps**: each step of the execution is performed after user confirmation, making 
possible to see the internal state of the LMC when running

---

## Structure

The project is structured in the following classes/modules:
- **Assembler**: it is the component that, given a `.lmc` source code file,
outputs the initial memory state of the LMC. It translates assembly
instructions to machine code instructions
- **LMC**: the core component that, given an initial memory state, an execution
mode and optional inputs, executes the program.
- **Main**: the compilation and execution entry point
- **Exceptions**: this module contains all the necessary custom exceptions
- **Queue**: a separate class for the queue implementation. Useful since the 
LMC has an input and an output queue

---

## Usage

### Compiling and Running

The program compiles and runs the `.lmc`in a single command. the format has
to be the following

`python3 <path-to-main.py> <path-to-lmc-source> --input <input-values> --mode <standard/steps>` 

The projects already contains some sources examples. A quick test can be made by pasting the following:

`python3 main.py lmc/multiplication.lmc --input 12 12 --mode standard`