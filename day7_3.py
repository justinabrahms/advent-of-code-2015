import operator
import unittest
import re
from pprint import pprint

mask = 2 ** 16 - 1
instruction_parser = re.compile('(?P<commands>.*) -> (?P<wire>\w+)$')
flat_letter = re.compile('^(?P<letter>\w+)$')
flat_number = re.compile('^(?P<number>\d+)$')
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

schwern = """q AND r -> x
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""

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
        instruction = instruction.strip()
        if wire in done:
            continue
        print wire
        if wire == 's':
            print '@@@ %s ' % (locals(),)
        # Flat
        num_result = flat_number.search(instruction)
        letter_result = flat_letter.search(instruction)
        binary_result = binary_re.search(instruction)
        unary_result = unary_re.search(instruction)
        if num_result:
            print "Num"
            done[wire] = int(num_result.group()) & mask

        elif letter_result:
            print "letter"
            letter = letter_result.group()
            if letter in done:
                done[wire] = done.get(letter) & mask

        # binary
        elif binary_result:
            print "binary"
            first, oper, second = binary_result.groups()
            if wire == 's':
                print 'ZZZZZ %s' % (locals(),)

            if (first in done or flat_number.match(first)) and \
               (second in done or flat_number.match(second)):
                print "running {} on {} and {}".format(
                    oper,
                    int(done.get(first, first)) & mask,
                    int(done.get(second, second)) & mask)
                done[wire] = BINARY_MAPPING[oper](
                    int(done.get(first, first)) & mask,
                    int(done.get(second, second)) & mask
                ) & mask

        elif unary_result:
            print "unary"
            oper, num = unary_result.groups()
            if num in done or flat_number.match(num):
                done[wire] = UNARY_MAPPING[oper](int(done.get(num, num)) & mask) & mask
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

    def test_crazy_defaults(self):
        done = {}
        self.assertEqual(2, int(done.get('2', '2')))

    def test_while_loop(self):
        result = {}
        while 'h' not in result:
            result = do_it(result, start)
            
        self.assertEqual(result['h'], 65412)

    def test_shwern_is_wrong(self):
        cmds = """
123 -> x
NOT x -> y"""
        self.assertEqual(do_it({}, cmds)['y'], ~123 & (2**16-2))
        
    def test_letter(self):
        result = {}
        while 'y' not in result:
            result = do_it(result, "x -> y\n9 -> x")
        self.assertEqual(result['y'], 9)

    def test_dict_changes(self):
        result = {}
        new_one = result.copy()
        new_one = do_it(new_one, "1 -> x")

        self.assertTrue('x' not in result)
        self.assertTrue('x' in new_one)
        

    def test_broken(self):
        self.assertRaises(AttributeError, lambda: do_it({}, "zargob felmeth -> x"))

    def test_missing_unary(self):
        instruction = "NOT x -> h\n123 -> x"
        result = do_it(do_it({}, instruction), instruction)
        self.assertEqual(result['h'], 65412)

    def test_maybe_thank_schwern(self):
        result = {}
        count = 0
        instructions = """
v OR w -> x
x RSHIFT 3 -> z
b RSHIFT 1 -> v
s LSHIFT 15 -> w
1 AND r -> s
o AND q -> r
b OR n -> o
k AND m -> n
d OR j -> k
b RSHIFT 2 -> d
g AND i -> j
e OR f -> g
NOT h -> i
e AND f -> h
b RSHIFT 3 -> e
b RSHIFT 5 -> f
19138 -> b
NOT l -> m
d AND j -> l
NOT p -> q
b AND n -> p"""
        
        while True:
            count += 1
            result = do_it(result, instructions)
            if count > 1000:
                break

        self.assertEqual(result['b'], 19138)
        self.assertEqual(result['d'], 4784)
        self.assertEqual(result['e'], 2392)
        self.assertEqual(result['f'], 598)
        self.assertEqual(result['g'], 2910)
        self.assertEqual(result['h'], 80)
        self.assertEqual(result['i'], 65455)
        self.assertEqual(result['j'], 2830)
        self.assertEqual(result['k'], 7102)
        self.assertEqual(result['l'], 512)
        self.assertEqual(result['m'], 65023)
        self.assertEqual(result['n'], 6590)
        self.assertEqual(result['o'], 23550)
        self.assertEqual(result['p'], 2178)
        self.assertEqual(result['q'], 63357)
        self.assertEqual(result['r'], 21372)
        self.assertEqual(result['s'], 0)
        self.assertEqual(result['v'], 9569)
        self.assertEqual(result['w'], 0)
        self.assertEqual(result['x'], 9569)
        self.assertEqual(result['z'], 1196)

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
    # result = {}
    # instructions = open('day7.txt').read()
    # loops = 0
    # while 'a' not in result:
    #     result = do_it(result, instructions)
    # print 'DAY 1 FINAL ANSWER: %s' % result['a']


    result = {}
    instructions = open('day7.b.txt').read()
    loops = 0
    while 'a' not in result:
        result = do_it(result, instructions)
    print 'DAY 2 FINAL ANSWER: %s' % result['a']
