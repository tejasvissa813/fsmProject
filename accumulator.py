import pyrtl
from fsm import FSM
from enum import Enum

input_wire = pyrtl.Input(bitwidth=2, name="input")
output_temp = pyrtl.WireVector(bitwidth=2, name="output_temp")
output = pyrtl.Output(bitwidth=10, name="output")

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
    "all + 0 -> GO",
    "GO + 1 -> STOP",
    "GO + 2 -> GO",
    "STOP + 1 -> STOP",
    "STOP + 2 -> RESET",
    "RESET + 1 -> RESET",
    "RESET + 2 -> RESET"
]
acc_states_list = ["GO", "STOP", "RESET"]
acc_state = FSM(states=acc_states_list, input_bitwidth=2, rulesList=acc_state_rules)
accumulator = pyrtl.Register(bitwidth=8)

acc_state <<= input_wire
output_temp <<= acc_state()

with pyrtl.conditional_assignment:
    with output_temp == 0:
        accumulator.next |= accumulator + 1
    with output_temp == 1:
        accumulator.next |= accumulator
    with output_temp == 2:
        accumulator.next |= 0

output <<= accumulator

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

sim_inputs = {
    'input' : '000010110112001'
}
sim.step_multiple(sim_inputs)
sim_trace.render_trace(trace_list=['input', 'output_temp', 'output'])

