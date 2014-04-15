#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
from itertools import chain
import sys

#DICTIONARY_PATH = 'dictionary.txt'
#DICTIONARY_PATH = 'dictionary-500.txt'
DICTIONARY_PATH = 'dictionary-3000.txt'


def levenshtein(word_a, word_b):
    if len(word_a) < len(word_b):
        return levenshtein(word_b, word_a)

    if len(word_b) == 0:
        return len(word_a)

    previous_row = xrange(len(word_b) + 1)
    for i, c1 in enumerate(word_a):
        current_row = [i + 1]
        for j, c2 in enumerate(word_b):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


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
        proposals = propose(word, dictionary)
        print ", ".join(proposals)


def propose(mistake, dictionary):
    best_words = None
    best_distance = sys.maxint
    for word in dictionary:
        distance = levenshtein(mistake, word)
        if best_distance > distance:
            best_distance = distance
            best_words = [word]
        elif best_distance == distance:
            best_words.append(word)

    return list(set(best_words))

if __name__ == "__main__":
    main()