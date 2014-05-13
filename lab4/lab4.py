#!/usr/bin/env python

import fileinput
from plp import PLP


def safe_forms(p, i):
    try:
        return p.forms(i)
    except UnicodeDecodeError:
        return []


def main():
    words = [line.decode('utf-8').strip() for line in fileinput.input()]

    p = PLP()
    p.safe_forms = safe_forms

    i = 16777216
    #last = 18663968
    last = 16780000

    a_tergo = set()
    while i <= last:
        forms = safe_forms(p, i)
        forms = map(lambda form: form[::-1], forms)
        a_tergo.update(forms)
        i += 1

    for word in words:
        stemmed_word = word

        rec_list = p.rec(word)
        if rec_list:
            stemmed_word = p.bform(rec_list[0])

        print "{0},{1}".format(word.encode("utf-8"), stemmed_word.encode("utf-8"))

if __name__ == '__main__':
    main()
