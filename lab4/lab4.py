#!/usr/bin/env python

import fileinput
from plp import PLP
import re

import itertools
import pickle
import marisa_trie


from collections import Counter


def most_common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]


def getcommonstart(string1, string2):
    return ''.join(map(lambda x: x[0], itertools.takewhile(lambda (letter1, letter2): letter1 == letter2,
                                          itertools.izip(string1, string2))))

def most_common(lst):
    return max(set(lst), key=lst.count)


def prefixes(word):
    for i in xrange(len(word)):
        yield word[:i]


def to_value(bytes):
    return pickle.loads(bytes)


def find_best_match(a_tergo, word):
    for prefix in reversed(list(prefixes(word))):
        matching_items = a_tergo.items(prefix)

        #print matching_items

        if matching_items:
            values = map(lambda x: to_value(x[1]), matching_items)
            return most_common(values)


def main():
    words = [line.decode('utf-8').strip() for line in fileinput.input()]

    p = PLP()

    with open('atergo.pickled8') as atergo_file:
        a_tergo = pickle.load(atergo_file)

    for word in words:
        rec_list = p.rec(word)
        #if rec_list:
        #    stemmed_word = p.bform(rec_list[0])
        #else:

        match = find_best_match(a_tergo, word[::-1])
        stemmed_word = re.sub(match[0] + '$', match[1], word)

        print "{0},{1}".format(word.encode("utf-8"), stemmed_word.encode("utf-8"))

if __name__ == '__main__':
    main()
