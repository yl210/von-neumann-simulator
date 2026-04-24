import sys

from core.register import Register, ProgramCounter, InstructionRegister
from core.ram import RAM
from core.mux import MUX
from core.demux import DEMUX
from core.decoder import Decoder
from core.alu import ALU
from core.utils import *

def initGPR():
    gpr = []
    r0 = Register(None)
    r1 = Register(None)
    r2 = Register(None)
    r3 = Register(None)
    gpr.extend([r0, r1, r2, r3])
    return gpr

# CPU CYCLE FEATURE: fetch, decode, execute functions
def fetch(pc, ir, ram):
    currentAddress = pc.getCounter()
    ram_data = ram.read_from_ram(currentAddress)

    if ram_data != None:
        ir.load_new_instruction(ram_data)
        ir_data = ir.read_from_ir()
        ir.set_opcode(ir_data)
        ir.set_operand(ir_data)
        pc.increment_counter()
    else:
        # claude: error handling
        raise ValueError('no data stored at address')

def decode(dc, op):
    return (op, dc[op])

def execute(dc_out, ir_data, gpr, ram, mux, demux, ir, alu, pc):
    selected = dc_out[0]

    # registers
    if selected < 4:
        active_reg = gpr[selected]
        if selected == 0 and alu.outputs != dict():
            active_reg.write_to_reg(alu.outputs[alu.output_type])
        else:
            data = ram.read_from_ram(ir.operand)
            active_reg.write_to_reg(data)

    # mux
    elif selected == 4:
        mux_input = ir.operand
        register_num = mux.get_linked_register(mux_input)
        mux.set_mux_output(gpr[register_num])

    # demux
    elif selected == 5:
        ope = ir.operand
        demux_data = mux.get_mux_output()
        demux.store_demux_input(get_lsb(ope), demux_data)
    
    # add
    elif selected == 6:
        a = demux.get_data(0)
        b = demux.get_data(1)
        if alu.has_valid_inputs(a, b):
            alu.output_type = alu.add()

    # subtract
    elif selected == 7:
        a = demux.get_data(0)
        b = demux.get_data(1)
        if alu.has_valid_inputs(a, b):
            alu.output_type = alu.sub()

    # N-flag
    elif selected == 8:
        if not alu.is_negative():
            pc.set_counter(ir.operand)

    # read from r0, write to ram
    elif selected == 9:
        active_reg = gpr[0]
        data = active_reg.read_reg()
        ram.write_to_ram(ir.operand, data)