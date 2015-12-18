import operator
import unittest
import re
from pprint import pprint

mask = 2 ** 16 - 1
instruction_parser = re.compile('(?P<commands>.*) -> (?P<wire>\w+)$')
flat_letter = re.compile('^(?P<letter>\w+)$')
flat_number = re.compile('^(?P<number>\d+)')
binary_re = re.compile('^(?P<first>\w+) (?P<bitwise>\w+) (?P<second>\w+)')
unary_re = re.compile('^(?P<unary>[NOT]+) (?P<first>\w+)')

BINARY_MAPPING = {
    'AND': operator.and_,
    'OR': operator.or_,
    'RSHIFT':operator.rshift,
    'LSHIFT': operator.lshift,
}

UNARY_MAPPING = {
    'NOT': operator.inv
}

# start = """
# 456 -> y
# x AND y -> d
# x OR y -> e
# x LSHIFT 2 -> f
# NOT x -> h
# 123 -> x"""

start = """
456 -> y
x AND y -> d
x OR y -> e
123 -> x
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""


def do_it(done, todo):
    for line in todo.split('\n'):
        if len(line.strip()) == 0:
            continue
        instruction, wire = instruction_parser.search(line).groups()
        if wire in done:
            continue

        # Flat
        num_result = flat_number.search(instruction)
        letter_result = flat_letter.search(instruction)
        binary_result = binary_re.search(instruction)
        unary_result = unary_re.search(instruction)
        if num_result:
            done[wire] = int(num_result.group()) & mask

        elif letter_result:
            letter = letter_result.group()
            if letter in done:
                done[wire] = done.get(letter)

        # binary
        elif binary_result:
            first, op, second = binary_result.groups()
            if (first in done or flat_number.match(first)) and \
               (second in done or flat_number.match(second)):
                done[wire] = BINARY_MAPPING[op](int(done.get(first, first)), int(done.get(second, second))) & mask

        elif unary_result:
            oper, num = unary_result.groups()
            if num in done or flat_number.match(num):
                done[wire] = UNARY_MAPPING[oper](int(done.get(num, num))) & mask
        else:
            raise AttributeError("WTF? %s" % instruction)    
    return done

class DoItTests(unittest.TestCase):
    def test_replaces_the_first_iteration(self):
        a = do_it({},  start)
        self.assertEqual(a['x'], 123)
        self.assertEqual(a['y'], 456)

    def test_replaces_the_second(self):
        a = do_it({},  start)
        self.assertEqual(a['x'], 123)

        d = do_it(a, start)
        self.assertEqual(d['d'], 72)
        self.assertEqual(d['f'], 492)

        g = do_it(d, start)
        self.assertEqual(g['h'], 65412)

    def test_while_loop(self):
        result = {}
        while 'h' not in result:
            result = do_it(result, start)
            
        self.assertEqual(result['h'], 65412)

    def test_letter(self):
        result = {}
        while 'y' not in result:
            result = do_it(result, "x -> y\n9 -> x")
        self.assertEqual(result['y'], 9)

    def test_broken(self):
        self.assertRaises(AttributeError, lambda: do_it({}, "zargob felmeth -> x"))

    def test_missing_unary(self):
        instruction = "NOT x -> h\n123 -> x"
        result = do_it(do_it({}, instruction), instruction)
        self.assertEqual(result['h'], 65412)

    def test_example(self):
        result = {}
        total = 0
        while len(result.keys()) < 8:
            total += 1
            result = do_it(result, start)

        self.assertEqual(result['d'], 72)
        self.assertEqual(result['e'], 507)
        self.assertEqual(result['f'], 492)
        self.assertEqual(result['g'], 114)
        self.assertEqual(result['h'], 65412)
        self.assertEqual(result['i'], 65079)
        self.assertEqual(result['x'], 123)
        self.assertEqual(result['y'], 456)



if __name__ == '__main__':  # pragma: no cover
    result = {}
    instructions = open('day7.txt').read()
    loops = 0
    while 'a' not in result:
        result = do_it(result, instructions)
    print 'FINAL ANSWER: %s' % result['a']
