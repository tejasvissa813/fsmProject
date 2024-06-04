import pyrtl
from fsm import FSM
from enum import Enum

input_wire = pyrtl.Input(bitwidth=2, name="input")
state = pyrtl.Output(bitwidth=2, name="currentState")
output = pyrtl.Output(bitwidth=1, name="output")

##KEY##
## 00 = GO
## 01 = STOP
## 10 = RESET

# acc_state_rules = {
#     0b0000 : 0b00,
#     0b0001 : 0b01,
#     0b0010 : 0b00,
#     0b0100 : 0b00,
#     0b0101 : 0b01,
#     0b0110 : 0b10,
#     0b1000 : 0b00,
#     0b1001 : 0b10,
#     0b1010 : 0b10
# }

acc_state_rules = [
    "all + 0 -> GO, 1",
    "GO + 1 -> STOP, 0",
    "GO + 2 -> GO, 1",
    "STOP + 1 -> STOP, 0",
    "STOP + 2 -> RESET, 0",
    "RESET + 1 -> RESET, 0",
    "RESET + 2 -> RESET, 0"
]


acc_states_list = ["GO", "STOP", "RESET"]

acc_state = FSM(states=acc_states_list, input_bitwidth=2, output_bitwidth=1, rulesList=acc_state_rules)
acc_state <<= [input_wire, 0]


output <<= acc_state()[0]
state <<= acc_state()[1]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    'input' : '000010110112001'
}
sim.step_multiple(sim_inputs)
sim_trace.render_trace(trace_list=['input', 'currentState', 'output'])

