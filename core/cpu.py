import sys

from register import Register, ProgramCounter, InstructionRegister
from ram import RAM
from mux import MUX
from demux import DEMUX
from decoder import Decoder
from alu import ALU
from utils import *


def initGPR():
    gpr = []
    r0 = Register(None)
    r1 = Register(None)
    r2 = Register(None)
    r3 = Register(None)
    gpr.extend([r0, r1, r2, r3])
    return gpr

def fetch(pc, ir, ram):
    currentAddress = pc.getCounter()
    ram_data = ram.read_from_ram(currentAddress)

    if ram_data != None:
        ir.load_new_instruction(ram_data)
        ir_data = ir.read_from_ir()
        ir.set_opcode(ir_data)
        ir.set_operand(ir_data)
        print(f'ADDR:{pc.getCounter()}  OP: {bin(ir.opcode)}  OPE: {bin(ir.operand)}')
    pc.increment_counter()
    # how to bypass addresses with no data

    

def decode(dc, op):
    return (op, dc[op])

def execute(dc_out, ir_data, gpr, ram, mux, demux, ir, alu, pc):
    selected = dc_out[0]
    print(f'selected: {selected}')

    # registers
    if selected < 4:
        active_reg = gpr[selected]
        if selected == 0 and alu.outputs != dict():
            active_reg.write_to_reg(alu.outputs[alu.output_type])
        else:
            print(f'operand: {ir.operand}')
            data = ram.read_from_ram(ir.operand)
            print(f'ram_data: {data}')
            active_reg.write_to_reg(data)

    # mux
    elif selected == 4:
        mux_input = ir.operand #ir.get_operand(ir_data)
        register_num = mux.get_linked_register(mux_input)
        mux.set_mux_output(gpr[register_num])
        print(f'mux_output: {mux.get_mux_output()}')

    # demux
    elif selected == 5:
        ope = ir.operand #ir.get_operand(ir_data)
        demux_data = mux.get_mux_output()
        demux.store_demux_input(get_lsb(ope), demux_data)
    
    # add
    elif selected == 6:
        a = demux.get_data(0)
        b = demux.get_data(1)
        #print(f'a: {a}, b: {b}')
        if alu.has_valid_inputs(a, b):
            alu.output_type = alu.add()
            print(f'alu_output: {format_byte(alu.outputs[alu.output_type])}')

    # subtract
    elif selected == 7:
        a = demux.get_data(0)
        b = demux.get_data(1)
        #print(f'a: {a}, b: {b}')
        if alu.has_valid_inputs(a, b):
            alu.output_type = alu.sub()
            print(f'alu_output: {format_byte(alu.outputs[alu.output_type])}')

    # N-flag
    elif selected == 8:
        if not alu.is_negative():
            pc.set_counter(ir.operand)
            #print(f'counter: {pc.getCounter()}')
            #ir.load_new_instruction(pc.getCounter())

    # read from r0, write to ram
    elif selected == 9:
        active_reg = gpr[0]
        data = active_reg.read_reg()
        ram.write_to_ram(ir.operand, data)

def main():

    running = True
    fetching = False
    decoding = False
    executing = False

    gpr = initGPR()
    pc = ProgramCounter(0)
    ir = InstructionRegister(0)
    ram = RAM()
    mux = MUX()
    dc = Decoder()
    demux = DEMUX()
    alu = ALU()
    

    while running:

        fetching = not fetching

        if fetching:
            fetch(pc, ir, ram)
            fetching = not fetching

        decoding = not decoding
        
        if decoding:
            ir_data = ir.read_from_ir()
            op = ir.opcode #ir.get_opcode(ir_data)

            dc_output = decode(dc.get_decoder(), op)
            decoding = not decoding
        
        executing = not executing

        if executing:
            execute(dc_output, ir_data, gpr, ram, mux, demux, ir, alu, pc)
            executing = not executing

        if pc.getCounter() > len(ram.get_ram())-1:
            running = False

        print(f'gpr: {gpr}')
        print(f'demux: {demux.get_demux()}')
        print(f'ram: {repr(ram)}')
        print('\n')
    
if __name__ == '__main__':
    sys.exit(main())
