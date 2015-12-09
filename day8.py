import re
def calc_space(f):
    f = f.replace(' ', '').replace('\n', '')
    total_chars = len(f)

    non_escaped = total_chars - (
        f.count(r'\\') +
        f.count(r'\"') +
        (len(re.findall(r'\\x\d{2}', f)) * 3)
    )

    return total_chars - non_escaped

big_str = r"""
""
"abc"
"aaa\"aaa"
"\x27"
"""
