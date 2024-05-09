from pyrtl import PyrtlError, WireVector, Register, MemBlock, conditional_assignment, otherwise
from pyrtl.rtllib.muxes import sparse_mux
from pyrtl.corecircuits import concat, as_wires
from pyrtl.simulation import Simulation
from enum import Enum
from lark import Lark, Transformer
from abc import ABC, abstractmethod
import math

# class FSM:
#     def __init__(self, state_bitwidth, input_bitwidth, name=""):
#         self.state = pyrtl.Register(bitwidth=state_bitwidth)
#         self.input_bitwidth = input_bitwidth
#         self.state_bitwidth = state_bitwidth
#         self.rules = {} 
#         self.input = pyrtl.WireVector(bitwidth=input_bitwidth)
        
#     def __ilshift__(self, input_wire):
#         if len(input_wire) != self.input_bitwidth:
#             raise pyrtl.PyrtlError("Invalid Input")
#         self.input <<= input_wire
#         return self

#     def __ior__(self, input_wire):
#         if len(input_wire) != self.input_bitwidth:
#             raise pyrtl.PyrtlError("Invalid Input")
#         self.input <<= input_wire
#         return self

#     def __call__(self):
#         output = pyrtl.WireVector(bitwidth=self.state_bitwidth)
#         output <<= self.state
#         return output
    
#     def add_rule(self, current, inp, out):
#         from pyrtl.corecircuits import as_wires
#         if math.log(current+1,2) > self.state_bitwidth or math.log(out+1,2) > self.state_bitwidth:
#             raise pyrtl.PyrtlError("Invalid State Size")
#         if math.log(inp+1, 2) > self.input_bitwidth:
#             raise pyrtl.PyrtlError("Invalid Input Size")

#         self.rules[(as_wires(current), as_wires(inp))] = as_wires(out, bitwidth=self.state_bitwidth)
    
#     def run(self):
#         self.state.next <<= self.rules[(self.state, self.input)]

#sparse mux

# class FSM:
#     def __init__(self, input_bitwidth, state_bitwidth, rules):
#         self.input_bitwidth = input_bitwidth
#         self.state_bitwidth = state_bitwidth
#         self.state = Register(bitwidth=state_bitwidth)
#         self.input = WireVector(bitwidth=input_bitwidth)
#         self.rules = rules

#     def __ilshift__(self, wire):
#         if len(wire) != self.input_bitwidth:
#             raise PyrtlError("Invalid Input Bitwidth")
#         self.input <<= wire
#         self.state.next <<= sparse_mux(concat(self.state, self.input), self.rules)
#         return self
    
#     def __ior__(self, wire):
#         if len(wire) != self.input_bitwidth:
#             raise PyrtlError("Invalid Input Bitwidth")
#         self.input <<= wire
#         self.state.next <<= sparse_mux(concat(self.state, self.input), self.rules)
#         return self
    
#     def __call__(self):
#         return self.state


#enums and parsing

#Grammar for Rules
#state + input -> state
#STRING " + " INT " -> " STRING

class RuleTransformer(Transformer):
    def __init__(self, input_bitwidth, states):
        self.input_bitwidth = input_bitwidth
        self.states = states

    def state(self, wordList):
        return wordList[0]

    def input(self, intList):
        return int(intList[0])
    
    def output(self, outList):
        return int(outList[0])
            
    def start(self, rule):
        if rule[0] == "all":
            rulesUpdate = {}
            outputsUpdate = {}
            for state in self.states:
                stateInBits = self.states.index(state)
                key = (stateInBits << self.input_bitwidth) | rule[1]
                rulesUpdate.update({key : self.states.index(rule[2])})
                outputsUpdate.update({key : rule[3]})

            return [rulesUpdate, outputsUpdate]
        else:
            stateInBits = self.states.index(rule[0])
            key = (stateInBits << self.input_bitwidth) | rule[1]
            return [{key : self.states.index(rule[2])}, {key : rule[3]}]
            

class FSM:
    def __init__(self, input_bitwidth, output_bitwidth, states, rulesList):
        self.state_bitwidth = math.floor(math.log(len(states))+1)
        self.input_bitwidth = input_bitwidth
        self.state = Register(bitwidth=self.state_bitwidth)
        self.input_wire = WireVector(bitwidth=self.input_bitwidth)
        self.output = Register(bitwidth=output_bitwidth)
        self.stateList = states

        rule_grammar = '''
            start : state " + " input " -> " state ", " output
            state : WORD
            input : INT
            output : INT
            %import common.INT
            %import common.WORD
        '''
        rule_parser = Lark(rule_grammar)

        self.rules = {}
        self.outputs = {}
        for rule in rulesList:
            rule_tree = rule_parser.parse(rule)
            newRules = RuleTransformer(input_bitwidth, states).transform(rule_tree)
            self.rules.update(newRules[0])
            self.outputs.update(newRules[1])

        
         
    def __ilshift__(self, wire):
        if len(wire) != self.input_bitwidth:
            raise PyrtlError("Invalid Input Bitwidth")
        self.input_wire <<= wire
        self.state.next <<= sparse_mux(concat(self.state, self.input_wire), self.rules)
        self.output.next <<= sparse_mux(concat(self.state, self.input_wire), self.outputs)
        return self

    def __ior__(self, wire):
        if len(wire) != self.input_bitwidth:
            raise PyrtlError("Invalid Input Bitwidth")
        self.input_wire |= wire
        self.state.next <<= sparse_mux(concat(self.state, self.input_wire), self.rules)
        self.output.next <<= sparse_mux(concat(self.state, self.input_wire), self.outputs)
        return self
    
    def __call__(self):
        return [self.output, self.state]

#NEXT:
# 1) * to represent all states in the grammar  [done]
# 2) dictionary to define outputs on each state  []
# 3) Multiple input FSM? (ex. RESET WIRE)
# 4) Make a repo [done]
