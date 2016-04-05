import re
from collections import defaultdict


parser = re.compile(r'(?P<action>[\w\s]+) (?P<start>\d+,\d+) through (?P<end>\d+,\d+)')


z = parser.search('turn on 0,0 through 999,999').groupdict()
assert z['action'] == 'turn on', z['action']
assert z['start'] == '0,0'
assert z['end'] == '999,999'

def do_instruction(state, action, xs, ys):
    start_x, end_x = xs
    start_y, end_y = ys

    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            key = '{},{}'.format(x, y)
            if action == 'turn on':
                state[key] = True
            if action == 'turn off':
                if key in state:
                    del state[key]
            if action == 'toggle':
                if key in state:
                    del state[key]
                else:
                    state[key] = True
    return state

def light_show(instructions, impl, start_state={}):
    state = start_state
    for instruction in instructions:
        result = parser.search(instruction).groupdict()
        start_x, start_y = result['start'].split(',')
        end_x, end_y = result['end'].split(',')
        start_x = int(start_x)
        start_y = int(start_y)
        end_x = int(end_x)
        end_y = int(end_y)
        state = impl(
            state,
            action=result['action'],
            xs=(start_x, end_x),
            ys=(start_y, end_y))
    return state

z = light_show([
    'turn on 0,0 through 999,999',
    'toggle 0,0 through 999,0',
], do_instruction)

assert '10,0' not in z


def do_instruction__updated(state, action, xs, ys):
    start_x, end_x = xs
    start_y, end_y = ys

    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            key = '{},{}'.format(x, y)
            if action == 'turn on':
                state[key] += 1
            if action == 'turn off':
                state[key] -= 1
                if state[key] < 0:
                    state[key] = 0
            if action == 'toggle':
                state[key] += 2
    return state

# y = light_show([
#     'turn on 0,0 through 0,0'
# ], do_instruction__updated, start_state=defaultdict(int))

# assert sum(y.values()) == 1

# y = light_show([
#     'toggle 0,0 through 999,999'
# ], do_instruction__updated, start_state=defaultdict(int))

# assert sum(y.values()) == 2000000

y = light_show([
    'turn on 0,0 through 0,0',
    'toggle 0,0 through 999,999'
], do_instruction__updated, start_state=defaultdict(int))


with open('../../totallygloria/PythonProblems/AdventOfCode.06.data.py', 'r') as f:
        lines = f.readlines()

print sum(light_show(lines, do_instruction).values())

        