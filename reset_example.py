import pyrtl
from fsm import FSM
from enum import Enum

# pyrtl.core.set_debug_mode()

input_wire = pyrtl.Input(bitwidth=1, name="input")
reset_wire = pyrtl.Input(bitwidth=1, name="reset")
state = pyrtl.Output(bitwidth=2, name="currentState")
output = pyrtl.Output(bitwidth=1, name="output")

rules = [
    "A + 0 -> A, 0",
    "B + 0 -> B, 1",
    "C + 0 -> C, 0",
    "A + 1 -> B, 0",
    "B + 1 -> C, 0",
    "C + 1 -> A, 0"
]
set_of_states = ["A","B","C"]

example_machine = FSM(input_bitwidth=1, output_bitwidth=1, states=set_of_states, rulesList=rules, reset=reset_wire)
example_machine <<= input_wire

output <<= example_machine()[0]
state <<= example_machine()[1]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    'input' : '001000100000',
    'reset' : '000010000000'
}
sim.step_multiple(sim_inputs)
sim_trace.render_trace(trace_list=['input', 'reset', 'currentState', 'output'])