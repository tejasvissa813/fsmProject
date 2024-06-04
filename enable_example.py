import pyrtl
from fsm import FSM

i = pyrtl.Input(bitwidth=1, name="input")
o = pyrtl.Output(bitwidth=1, name="output")
e = pyrtl.Input(bitwidth=1, name="enable")

ex_states = ["A", "B", "C"]
ex_rules = [
    "A + 0 -> A, 1",
    "A + 1 -> B, 1",
    "B + 0 -> B, 1",
    "B + 1 -> C, 1",
    "C + 0 -> C, 1",
    "C + 1 -> A, 1",
]

ex_machine = FSM(input_bitwidth=1, output_bitwidth=1, states=ex_states, rulesList=ex_rules, enable=e)
ex_machine <<= i
o <<= ex_machine()[0]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    'input' : '111111101110111100000',
    'enable' : '111111111000000000000'
}
sim.step_multiple(sim_inputs)
sim_trace.render_trace(trace_list=['input', 'enable', 'output'])


