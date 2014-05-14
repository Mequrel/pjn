#!/usr/bin/env python

__author__ = 'mequrel'

from plp import PLP
import itertools
import pickle
import marisa_trie
from itertools import chain

def getcommonstart(string1, string2):
    return ''.join(map(lambda x: x[0], itertools.takewhile(lambda (letter1, letter2): letter1 == letter2,
                                          itertools.izip(string1, string2))))


def forms_to_changes(forms, p, i):
    for form in forms:
        base = p.bform(i)
        common_prefix = getcommonstart(base, form)
        remove = form[len(common_prefix):]
        add = base[len(common_prefix):]

        yield (form[::-1], (remove, add))


def safe_forms(p, i):
    try:
        return forms_to_changes(p.forms(i), p, i)
    except UnicodeDecodeError:
        return []


def to_bytes(value):
    return pickle.dumps(value)


def generate_for_i(p, i):
    forms = safe_forms(p, i)
    return map(lambda (k, v): (k, to_bytes(v)), forms)


def main():
    p = PLP()

    first = 16777216
    last = 18663968
    #last = 17000000

    a_tergo = chain.from_iterable(generate_for_i(p, i) for i in xrange(first, last+1))

    a_tergo = marisa_trie.BytesTrie(a_tergo)

    with open('atergo_all.pickled', 'w') as atergo_file:
        pickle.dump(a_tergo, atergo_file)

if __name__ == '__main__':
    main()
