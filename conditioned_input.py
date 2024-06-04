import pyrtl
from fsm import FSM

input_1 = pyrtl.Input(bitwidth=1, name='1')
input_2 = pyrtl.Input(bitwidth=1, name='2')
input_3 = pyrtl.Input(bitwidth=1, name='3')
output = pyrtl.Output(bitwidth=1, name='o')

ex_states = ["A", "B", "C"]
ex_rules = [
    "A + 0 -> A, 0",
    "A + 1 -> C, 1",
    "B + 0 -> B, 0",
    "B + 1 -> B, 1",
    "C + 0 -> A, 0",
    "C + 1 -> C, 1"
]

ex_machine = FSM(input_bitwidth=1, output_bitwidth=1, states=ex_states, rulesList=ex_rules)
with pyrtl.conditional_assignment:
    with input_1:
        ex_machine |= input_2
    with pyrtl.otherwise:
        ex_machine |= input_3

output <<= ex_machine()[0]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    '1' : '11111111111000000110000',
    '2' : '01010101011111111111111',
    '3' : '00000000000000000000000'
}
sim.step_multiple(sim_inputs)
sim_trace.render_trace(trace_list=['1', '2', '3', 'o'])



