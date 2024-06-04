import pyrtl
from fsm import FSM

input_wire = pyrtl.Input(bitwidth=1, name="input")
output_wire = pyrtl.Output(bitwidth=3, name="output")
vending_machine_states = ["WAIT", "TOKONE", "TOKTWO", "TOKTHREE", "DISP", "RFND"]
vending_machin_rules = [
    "all + 0 -> RFND, 0",
    "WAIT + 1 -> TOKONE, 1",
    "TOKONE + 1 -> TOKTWO, 2",
    "TOKTWO + 1 -> TOKTHREE, 3",
    "TOKTHREE + 1 -> DISP, 4",
    "DISP + all -> WAIT, 0",
    "RFND + all -> WAIT, 0"
]

vending_machine = FSM(input_bitwidth=1, output_bitwidth=3, states=vending_machine_states, rulesList=vending_machin_rules)
vending_machine <<= input_wire
output_wire <<= vending_machine()[0]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    'input' : '111111101110111100000'
}
sim.step_multiple(sim_inputs)
sim_trace.render_trace(trace_list=['input', 'output'])



