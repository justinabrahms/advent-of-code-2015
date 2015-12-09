import hashlib

def checker(term, prefix):
    return hashlib.md5(term).hexdigest().startswith(prefix)

def gen(key, prefix='00000'):
    num = 1
    while not checker("{}{}".format(key,num), prefix):
        num += 1
    return num

assert 609043 == gen('abcdef')
assert 1048970 == gen('pqrstuv')
