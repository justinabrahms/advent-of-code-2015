from unittest import TestCase, skip
import re
import operator
import logging
logging.basicConfig()

log = logging.getLogger(__name__)

start = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""
end = """d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456
"""

instructions = start.split('\n')
result = end

instruction_parser = re.compile('(?P<commands>.*) -> (?P<wire>\w+)$')

def parse_instruction(instruction):
    found = instruction_parser.search(instruction)
    if found:
        return found.groupdict()['commands'], found.groupdict()['wire']

BINARY_MAPPING = {
    'AND': operator.and_,
    'OR': operator.or_,
    'RSHIFT':operator.rshift,
    'LSHIFT': operator.lshift,
}

UNARY_MAPPING = {
    'NOT': operator.inv
}


def instruction_to_result(state, instruction, wire):
    mask = 2 ** 16 - 1
    flat_number = re.search('^(?P<number>\d+)', instruction)
    binary_re = re.search('^(?P<first>\w+) (?P<bitwise>\w+) (?P<second>\w+)', instruction)
    unary_re = re.search('^(?P<unary>[NOT]+) (?P<first>\w+)', instruction)
    if flat_number:
        num = int(flat_number.groupdict()['number'])
        log.debug("FLAT NUMBER: {} {}".format(wire, num))
        state[wire] = num
    elif binary_re:
        first, bitwise, second = binary_re.groups()
        first = state.get(first, first)
        second = state.get(second, second)
        fn = BINARY_MAPPING[bitwise]
        log.debug("Mapping {} via {} {} {}".format(wire, first, bitwise, second))
        state[wire] = fn(int(first), int(second)) & mask
    elif unary_re:
        parsed = unary_re.groupdict()
        first = parsed['first']
        log.debug("UNARY: {} via {} {} (val: {})".format(wire, parsed['unary'], first, int(state.get(first, first)) & mask))
        state[wire] = UNARY_MAPPING[parsed['unary']](int(state.get(first, first))) & mask
    else:
        raise NotImplemented()
    return state

def main(instructions):
    state = {}
    for i in instructions.split("\n"):
        instruction, wire = parse_instruction(i)
        state = instruction_to_result(state, instruction, wire)
    keys = sorted(state.keys())
    result = ""
    for k in keys:
        result += "{}: {}\n".format(k, state[k])
    return result

class InstructionTest(TestCase):
    def test_run_wire_value(self):
        state = instruction_to_result({}, '1234', 'x')
        self.assertEqual(state['x'], 1234)
        
    def test_run_and(self):
        "bitwise and test"
        state = instruction_to_result({'x': 3, 'y': 5}, 'x AND y', 'z')
        self.assertEqual(state['z'], 1)
        
    def test_run_not(self):
        state = instruction_to_result({'x': 123}, 'NOT x', 'y')
        self.assertEqual(state['y'], 65412)
    
    def test_parses_wire_from_stream(self):
        _, wire = parse_instruction(instructions[0])
        self.assertEqual(wire, 'x')
        
    def test_parses_instructions(self):
        commands, _ = parse_instruction(instructions[0])
        self.assertEqual('123', commands)
        
    def test_input_is_output(self):
        ret = main(start)
        self.assertEqual(ret, end, "{} \n !=\n {}".format(ret, end))