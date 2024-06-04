import pyrtl
from fsm import FSM

valid = pyrtl.Input(bitwidth=1, name="valid")
ready = pyrtl.Input(bitwidth=1, name="ready")

m1_out = pyrtl.WireVector(bitwidth=1, name="m1_out")
m2_out = pyrtl.WireVector(bitwidth=1, name="m2_out")
transfer = pyrtl.Output(bitwidth=1, name="output")

m1_in = pyrtl.WireVector(bitwidth=2, name="m1_in")
m2_in = pyrtl.WireVector(bitwidth=2, name="m2_in")
m1_in <<= pyrtl.corecircuits.concat(valid, m2_out)
m2_in <<= pyrtl.corecircuits.concat(ready, m1_out)

m1_states = ["Inactive", "Waiting", "Active"]
m1_rules = [
    "all + 0 -> Inactive, 0",
    "all + 1 -> Inactive, 0",
    "all + 2 -> Waiting, 0",
    "all + 3 -> Active, 1",
]
m2_states = ["Inactive", "Waiting", "Active"]
m2_rules = [
    "all + 0 -> Inactive, 0",
    "all + 1 -> Inactive, 0",
    "all + 2 -> Waiting, 1",
    "all + 3 -> Active, 1"
]

machine1 = FSM(input_bitwidth=2, output_bitwidth=1, states=m1_states, rulesList=m1_rules)
machine2 = FSM(input_bitwidth=2, output_bitwidth=1, states=m2_states, rulesList=m2_rules)
machine1 <<= m1_in
machine2 <<= m2_in
m1_out <<= machine1()[0]
m2_out <<= machine2()[0]

with pyrtl.conditional_assignment:
    with machine1()[1] == 2:
        with machine2()[1] == 2:
            transfer |= 1
        with pyrtl.otherwise:
            transfer |= 0
    with pyrtl.otherwise:
        transfer |= 0

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    'valid' : '0010111111001111',
    'ready' : '0000000111111100'
}
sim.step_multiple(sim_inputs)
sim_trace.render_trace(trace_list=['valid', 'ready', 'm1_out','m2_out', 'output'])