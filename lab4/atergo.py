#!/usr/bin/env python

__author__ = 'mequrel'

from plp import PLP
import itertools
import pickle

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


def main():
    p = PLP()

    i = 16777216
    last = 18663968
    #last = 17000000

    a_tergo = []
    while i <= last:
        forms = safe_forms(p, i)
        a_tergo.extend(forms)
        i += 1

    with open('atergo.pickled', 'w') as atergo_file:
        pickle.dump(a_tergo, atergo_file)

if __name__ == '__main__':
    main()
