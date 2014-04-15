#!/usr/bin/env python

import fileinput
from itertools import chain

DICTIONARY_PATH = 'dictionary.txt'


def load_dictionary():
    with open(DICTIONARY_PATH) as f:
        #lines = f.readlines()
        lines = f.read().splitlines()
        split = map(lambda x: x.split(", "), lines)
        return chain.from_iterable(split)


def main():
    dictionary = list(load_dictionary())

    for word in fileinput.input():
        word = word.strip()
        print propose(word)


def propose(word):
    return word

if __name__ == "__main__":
    main()