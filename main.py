# Matteo Alessandro Fumis (IN2000249)

import argparse
from assembler import Assembler
from lmc import Lmc
from exceptions import (
    MemoryExceededException,
    EmptyQueueException,
    IllegalInstructionException,
    InvalidFileExtensionException,
)

"""
    Function main()

    Parameters:
    - None (explicitly)

    The function:
    1. Creates a parser to compile and execute a source file from command line
    2. Instantiates an assembler and by calling the assemble() function sets
        the initial lmc memory state
    3. Instantiates an lmc with the initial memory state and possible arguments 
        provided via command line
    4. Runs the program with the specified mode 
    """

def main():
    parser = argparse.ArgumentParser(
        description="LMC Simulator - Compile and execute LMC assembly programs"
    )
    parser.add_argument("filename", type=str, help="Path to the .lmc assembly file")
    parser.add_argument(
        "--mode",
        choices=["standard", "steps"],
        default="standard",
        help="Execution mode: standard (continuous) or steps (interactive)",
    )
    parser.add_argument(
        "--input",
        type=int,
        nargs="*",
        help="Input values to be placed in the input queue",
    )

    args = parser.parse_args()

    try:
        print(f"Assembling {args.filename}...")
        assembler = Assembler()
        memory = assembler.assemble(args.filename)
        print("Assembly completed successfully.")

        print("Initializing LMC machine...")
        lmc = Lmc(memory, args.input)

        print(f"Executing in {args.mode} mode...\n")
        lmc.run(args.mode)

        print(f"\nProgram output: {lmc.output_queue}\n")

    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
    except MemoryExceededException as e:
        print(f"Error: {e}")
    except IllegalInstructionException as e:
        print(f"Error: {e}")
    except EmptyQueueException as e:
        print(f"Error: {e}")
    except InvalidFileExtensionException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
