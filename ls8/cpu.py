"""CPU functionality."""

import sys


# class CPU:
#     """Main CPU class."""

#     def __init__(self):
#         """Construct a new CPU."""
#         self.ram = [0] * 256
#         self.reg = [0] * 8
#         self.pc = 0

#     def load(self, file):
#         """Load a program into memory."""

#         address = 0

#         # For now, we've just hardcoded a program:

#         with open(file, 'r') as f:
#             for line in f:
#                 if line.startswith('#') or line.startswith('\n'):
#                     continue
#                 else:
#                     instruction = line.split(' ')[0]
#                     self.ram[address] = int(instruction, 2)
#                     address += 1

#     def ram_read(self, mar):
#         return self.ram[mar]

#     def ram_write(self, mar, mdr):
#         self.ram[mar] = mdr

#     def alu(self, op, reg_a, reg_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[reg_a] += self.reg[reg_b]
#         # elif op == "SUB": etc
#         elif op == "MUL":
#             self.reg[reg_a] += self.reg[reg_b]
#         else:
#             raise Exception("Unsupported ALU operation")

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             # self.fl,
#             # self.ie,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()

#     def run(self):
#         """Run the CPU."""
#         LDI = 0b10000010
#         PRN = 0b01000111
#         HLT = 0b00000001
#         MUL = 0b10100010

#         running = True

#         while running:
#             ir = self.ram_read(self.pc)

#             if ir == HLT:
#                 running = False

#             if ir == PRN:
#                 reg = self.ram_read(self.pc + 1)
#                 print(self.reg[reg])
#                 self.pc += 2

#             if ir == LDI:
#                 reg_a = self.ram_read(self.pc + 1)
#                 reg_b = self.ram_read(self.pc + 2)
#                 self.reg[reg_a] = reg_b
#                 self.pc += 3

#             if ir == MUL:
#                 reg_a = self.ram_read(self.pc + 1)
#                 reg_b = self.ram_read(self.pc + 2)
#                 self.alu("MUL", reg_a, reg_b)
#                 self.pc += 3


HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

MUL = 0b10100010
ADD = 0b10100000


# Main CPU class
class CPU:
    # Construct a new CPU
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7  # stack pointer is always register 7

        self.dispatchtable = {
            MUL: self.mul,
            ADD: self.add,
            PRN: self.prn,
            LDI: self.ldi,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret
        }

    # Load a program into memory

    def load(self, file_name):
        address = 0

        with open(file_name, 'r') as f:
            for line in f:
                if line.startswith('#') or line.startswith('\n'):
                    continue
                else:
                    instruction = line.split(' ')[0]
                    self.ram[address] = int(instruction, 2)
                    address += 1

    # Read RAM at given address and return that value

    def ram_read(self, mar):
        return self.ram[mar]

    # Write a value at given address

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    # ALU operations

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    # Handy function to print out the CPU state.
    # You might want to call this from run() if you need help debugging.

    def trace(self):
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # Handle MUL

    def mul(self, reg_a, reg_b):
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    # Handle ADD

    def add(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    # Handle PRN instruction

    def prn(self, reg_a, reg_b):
        print(self.reg[reg_a])
        self.pc += 2

    # Handle LDI

    def ldi(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b
        self.pc += 3

    # Handle PUSH

    def push(self, reg_a, reg_b):
        self.sp -= 1
        self.ram_write(self.sp, self.reg[reg_a])
        self.pc += 2

    # Handle POP

    def pop(self, reg_a, reg_b):
        self.reg[reg_a] = self.ram_read(self.sp)
        self.sp += 1
        self.pc += 2

    # Handle CALL

    def call(self, reg_a, reg_b):
        self.sp -= 1
        self.ram_write(self.sp, self.pc + 2)
        self.pc = self.reg[reg_a]

    # Handle RET

    def ret(self, reg_a, reg_b):
        self.pc = self.ram_read(self.sp)
        self.sp += 1

    # Run the CPU

    def run(self):
        running = True

        while running:
            ir = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                running = False
            else:
                self.dispatchtable[ir](reg_a, reg_b)
