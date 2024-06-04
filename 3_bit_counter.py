import pyrtl
from fsm import FSM

direction = pyrtl.Input(bitwidth=1, name="input")
reset_wire = pyrtl.Input(bitwidth=1, name="reset")
result = pyrtl.Output(bitwidth=3, name="output")

counter_states = ["A", "B", "C", "D", "E", "F", "G", "H"]
counter_rules = [
    "A + 1 -> B, 1",
    "B + 1 -> C, 2",
    "C + 1 -> D, 3",
    "D + 1 -> E, 4",
    "E + 1 -> F, 5",
    "F + 1 -> G, 6",
    "G + 1 -> H, 7",
    "H + 1 -> A, 0",
    "A + 0 -> H, 7",
    "B + 0 -> A, 0",
    "C + 0 -> B, 1",
    "D + 0 -> C, 2",
    "E + 0 -> D, 3",
    "F + 0 -> E, 4",
    "G + 0 -> F, 5",
    "H + 0 -> G, 6",
]

counter_machine = FSM(input_bitwidth=1, output_bitwidth=3, states=counter_states, rulesList=counter_rules, reset=reset_wire)
counter_machine <<= direction
result <<= counter_machine()[0]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    'input' : '1111111111100000000000000',
    'reset' : '0000010000100001000010000'
}
sim.step_multiple(sim_inputs)
sim_trace.render_trace(trace_list=['input', 'reset', 'output'])
