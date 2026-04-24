# 18-100 von Neumann Computer Architecture Simulator

## Motivation
Von Neumann computer architecture is the foundation of most modern general-purpose computing. This is taught in 18-100 Introduction to ECE through a highly abstracted computer architecture model. As both a past-18100 student and current TA, the problem is that tracing through each step can tedious and error-prone as the steps are very intricate. So, I wanted to make a simulator which will function as a tool for helping students understand the basics of computer architecture and how it would work with stronger visualization.

## Basics of von Neumann Architecture
The components of von Neumann architecture are:
- RAM (random access memory: long-term storage for operating instructions and data
- registers: short-term storage for data used in executing operations
- instruction register: register that's only purpose is storing the current active instruction
- decoder: interpreting what is the next step
- mux: selects between multiple input lines (in this case, the registers)
- demux: 'routes' the data from the mux to the specified output (in this case, the arithmetic logic unit).
- arithmetic logic unit: the unit that we can specify to perform adding/subtracting/detecting 0, etc.
- program counter: keeps track of the current address we are reading from

## Moving Through the Computer

### Interpreting Instructions
Each data corresponding to an address is actually an instruction that tells the CPU what to do next in a specific format. For example, the instruction at address 1 is: 00011110. Each instruction is broken into two 4-bit sections. The first four bits are the op-code, which tell the decoder what to do. The last four bits are the operand, which tell the decoder what address in the RAM to read/write form. In this example:
- 0001 = 1 -> select R1 and write the data from the given address to it
- 1110 = 13 -> address of data in RAM
So taken together 0001 and 1110 mean: 'write the data from the 13th line in RAM into R1'

### Decoding Instructions
The decoder can take inputs from 0-9. In my program, here is the key in the Decoder class:
```
self.decoder = {
            0 : 'Writing to Register 0',
            1 : 'Writing to Register 1',
            2 : 'Writing to Register 2',
            3 : 'Writing to Register 3',
            4 : 'Storing to Multiplexer',
            5 : 'Storing to De-multiplexer',
            6 : 'Adding numbers in ALU',
            7 : 'Subtracting numbers in ALU',
            8 : 'Testing if result is negative',
            9 : 'Writing result to RAM',
        }
  ```




