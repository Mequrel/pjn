#!/usr/bin/env python

import fileinput
from plp import PLP
import re

import itertools


def allsame(seq):
    return min([elem==seq[0] for elem in seq]+[True])


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


def find_best_match(a_tergo, word):
    best = a_tergo[0]
    best_len = len(getcommonstart(best[0], word))

    for dict_element in a_tergo:
        common_prefix = getcommonstart(dict_element[0], word)

        if len(common_prefix) > best_len:
            best_len = len(common_prefix)
            best = dict_element

    return best


def main():
    words = [line.decode('utf-8').strip() for line in fileinput.input()]

    p = PLP()

    i = 16777216
    #last = 18663968
    last = 16780000

    a_tergo = set()
    while i <= last:
        forms = safe_forms(p, i)
        a_tergo.update(forms)
        i += 1

    a_tergo = list(a_tergo)

    for word in words:
        rec_list = p.rec(word)
        #if rec_list:
        #    stemmed_word = p.bform(rec_list[0])
        #else:

        match = find_best_match(a_tergo, word[::-1])
        stemmed_word = re.sub(match[1][0] + '$', match[1][1], word)

        print "{0},{1}".format(word.encode("utf-8"), stemmed_word.encode("utf-8"))

if __name__ == '__main__':
    main()
