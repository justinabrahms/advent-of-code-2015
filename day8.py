import unittest

def chr_count(string):
    return len(string) + 2, len(string.decode('string-escape'))

def chr_count_2(string):
    wrapping_quotes = 2
    return (
        len(string) + wrapping_quotes,
        len(string.encode('string-escape')) +
        wrapping_quotes +
        (wrapping_quotes * 2)  # escaped original wrapping quotes 
    )
    
def multi_solve(strs):
    z = [chr_count(x) for x in strs]
    total = 0
    for p, m in z:
        total += p
        total -= m
    return total


class StringTests_v2(unittest.TestCase):
    def test_empty(self):
        a,b = chr_count_2(r"")
        assert a == 2, a
        assert b == 6, b

    def test_abc(self):
        a,b = chr_count_2(r"abc")
        assert a == 5, a
        assert b == 9, b

    def test_escape_quote(self):
        a,b = chr_count_2(r"aaa\"aaa")
        # orig: 10, 7
        assert a == 10, a
        # orig 10 + 4 for quotes + 2 for escaping slash
        assert b == 16, b

    def test_unicode(self):
        a, b = chr_count_2(r'\x27')
        assert a == 6
        assert b == 11

    def test_multi_solve(self):
        result = multi_solve([
            r'',
            r'abc',
            r'aaa\"aaa',
            r'\x27',
        ])
        assert result == 12
        
class StringTests(unittest.TestCase):
    def test_empty(self):
        a,b = chr_count(r"")
        assert a == 2, a
        assert b == 0, b

    def test_abc(self):
        a,b = chr_count(r"abc")
        assert a == 5, a
        assert b == 3, b

    def test_escape_quote(self):
        a,b = chr_count(r"aaa\"aaa")
        assert a == 10, a
        assert b == 7, b

    def test_unicode(self):
        a, b = chr_count(r'\x27')
        assert a == 6
        assert b == 1

    def test_multi_solve(self):
        result = multi_solve([
            r'',
            r'abc',
            r'aaa\"aaa',
            r'\x27',
        ])
        assert result == 12

if __name__ == '__main__':
    with open('day8.txt', 'r') as f:
        data = f.readlines()
        # strip quotes.
        print multi_solve([x[1:-1] for x in data])
