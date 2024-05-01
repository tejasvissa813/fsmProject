import pyrtl
import fsm

input_wire = pyrtl.Input(bitwidth=1, name="input")
output_wire = pyrtl.Output(bitwidth=3, name="output")
vending_machine_rules = {
    0b0000 : 0b001,
    0b0001 : 0b001,
    0b0010 : 0b000,
    0b0011 : 0b010,
    0b0100 : 0b000,
    0b0101 : 0b011,
    0b0110 : 0b000,
    0b0111 : 0b100,
    0b1000 : 0b000,
    0b1001 : 0b101,
    0b1010 : 0b001,
    0b1011 : 0b001
}
vending_machine = fsm.FSM(input_bitwidth=1, state_bitwidth=3, rules=vending_machine_rules)
vending_machine <<= input_wire
output_wire <<= vending_machine()

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    'input' : '111111101110111100000'
}
sim.step_multiple(sim_inputs)
sim_trace.render_trace(trace_list=['input', 'output'])



