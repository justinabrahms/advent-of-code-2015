"""
Did this purposefully without regexes for fun
"""

def multi_vowel(word):
    total = 0
    for letter in 'aeiou':
        total += word.count(letter)
    return total >= 3
    
def double_letter(word):
    last_letter = word[0]
    for letter in word[1:]:
        if letter == last_letter:
            return True
        last_letter = letter
    return False

def forbidden_combo(word):
    is_forbidden = False
    for forbidden in ('ab', 'cd', 'pq', 'xy'):
        if forbidden in word:
            is_forbidden = True
    return is_forbidden

def is_nice(word):
    return multi_vowel(word) and double_letter(word) and not forbidden_combo(word)

assert is_nice('ugknbfddgicrmopn')
assert is_nice('aaa')
assert not is_nice('jchzalrnumimnmhp')
assert not is_nice('haegwjzuvuyypxyu')
assert not is_nice('dvszwmarrgswjxmb')


def new_repeat(word):
    offset = 3
    for x in range(len(word) - offset + 1):
        a, _, b = word[x:x+offset]
        if a == b:
            return True
    return False


def non_overlap_pairs(word):
    for x in range(len(word) - 1):
        to_check = word[x:x+2]
        if to_check in word[0:x] or to_check in word[x+2:]:
            return True
    return False

def new_is_nice(word):
    return new_repeat(word) and non_overlap_pairs(word)

assert new_is_nice('qjhvhtzxzqqjkmpb')
assert new_is_nice('xxyxx')
assert not new_is_nice('uurcxstgmygtbstg')
assert not new_is_nice('ieodomkazucvgmuy')