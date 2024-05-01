import pyrtl
from fsm import FSM

machine_1_rules = {
    0 : 0,
    1 : 0,
    2 : 0,
    4 : 1,
    5 : 1,
    6 : 1,
    8 : 0,
    9 : 0,
    10 : 0,
    12 : 1,
    13 : 2,
    14 : 2,
    16 : 0,
    17 : 0,
    18 : 0,
    20 : 1,
    21 : 2,
    22 : 2
}

machine_2_rules = {
    0 : 0,
    1 : 0,
    2 : 0,
    4 : 1,
    5 : 1,
    6 : 1,
    8 : 0,
    9 : 0,
    10 : 0,
    12 : 1,
    13 : 1,
    14 : 2,
    16 : 0,
    17 : 0,
    18 : 0,
    20 : 2,
    21 : 2,
    22 : 2
}

m1 = FSM(input_bitwidth=3, state_bitwidth=2, rules=machine_1_rules)
m2 = FSM(input_bitwidth=3, state_bitwidth=2, rules=machine_1_rules)

valid = pyrtl.Input(bitwidth=1, name="valid")
ready = pyrtl.Input(bitwidth=1, name="ready")

out_1 = pyrtl.WireVector(bitwidth=2, name="out_1")
out_2 = pyrtl.WireVector(bitwidth=2, name="out_2")

out_1 <<= m1()
out_2 <<= m2()

in_1 = pyrtl.WireVector(bitwidth=3, name="in_1")
in_2 = pyrtl.WireVector(bitwidth=3, name="in_2")

in_1 <<= pyrtl.corecircuits.concat(valid, out_2)
in_2 <<= pyrtl.corecircuits.concat(ready, out_1)

m1 <<= in_1
m2 <<= in_2

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    'valid' : '0010111111001111',
    'ready' : '0000000111111100'
}
sim.step_multiple(sim_inputs)
sim_trace.render_trace(trace_list=['valid', 'ready', 'out_1','out_2'])