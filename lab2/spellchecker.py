#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
from itertools import chain
import sys

#DICTIONARY_PATH = 'dictionary-3000.txt'
DICTIONARY_PATH = 'dictionary.txt'


def known_words(words, dictionary):
    return words.intersection(dictionary)


def generate_levenshtein(word, alphabet):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    inserts = [(a + c + b, 1) for a, b in splits for c in alphabet]
    deletes = [(a + b[1:], 1) for a, b in splits if b]
    replaces = [(a + c + b[1:], 1) for a, b in splits for c in alphabet if b]
    transposes = [(a + b[1] + b[0] + b[2:], 1) for a, b in splits if len(b) > 1]
    return set(inserts + deletes + replaces + transposes)


def levenshtein(word_a, word_b):
    if len(word_a) < len(word_b):
        return levenshtein(word_b, word_a)

    if len(word_b) == 0:
        return len(word_a)

    # if abs(len(word_a) - len(word_b)) > 3:
    #     return len(word_b) + 1

    p_previous_row = xrange(len(word_b) + 1)
    previous_row = xrange(len(word_b) + 1)
    for i, c1 in enumerate(word_a):
        mn = len(word_b) + 1
        current_row = [i + 1]
        for j, c2 in enumerate(word_b):
            insertions = previous_row[
                             j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            best = min(insertions, deletions, substitutions)

            if i > 0 and j > 0 and c1 == word_b[j - 1] and c2 == word_a[i - 1]:
                transpositions = p_previous_row[j - 1] + 0.5
                best = min(best, transpositions)

            mn = min(mn, best)
            current_row.append(best)

        # if mn >= 1.0:
        #     return len(word_b) + 1

        p_previous_row = previous_row
        previous_row = current_row

    return previous_row[-1]


def load_dictionary():
    with open(DICTIONARY_PATH) as f:
        #lines = f.readlines()
        lines = f.read().splitlines()
        split = map(lambda x: x.split(", "), lines)
        return chain.from_iterable(split)


def main():
    dictionary = set(load_dictionary())

    for word in fileinput.input():
        word = word.strip()
        word = word.decode("utf-8")
        proposals = propose2(word, dictionary)
        print u', '.join(proposals).encode("utf-8")


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


def propose2(mistake, dictionary):
    alphabet = u'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź'

    words = set(map(lambda x: x[0], generate_levenshtein(mistake, alphabet)))

    known1 = known_words(words, dictionary)

    return known1 or [mistake]


if __name__ == "__main__":
    main()