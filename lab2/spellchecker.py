#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections

import fileinput
from itertools import chain

#DICTIONARY_PATH = 'dictionary-3000.txt'
import re

DICTIONARY_PATH = 'dictionary.txt'




def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model



def words(text): return re.findall('[\w]+', text.lower(), flags=re.UNICODE)
NWORDS = train(words(file('korpus').read()))

def known_words(words, dictionary):
    return words.intersection(dictionary)


replace_cost = {}
replace_cost[(u'o', u'ó')] = 0.25
replace_cost[(u'a', u'ą')] = 0.25
replace_cost[(u'e', u'ę')] = 0.25
replace_cost[(u'n', u'ń')] = 0.25
replace_cost[(u's', u'ś')] = 0.25
replace_cost[(u'c', u'ć')] = 0.25
replace_cost[(u'l', u'ł')] = 0.25
replace_cost[(u'z', u'ź')] = 0.25
replace_cost[(u'z', u'ż')] = 0.25

replace_cost[(u'u', u'ó')] = 0.25
replace_cost[(u'rz', u'ż')] = 0.25
replace_cost[(u'ch', u'h')] = 0.25
replace_cost[(u'ę', u'em')] = 0.25
replace_cost[(u'ę', u'en')] = 0.25
replace_cost[(u'ą', u'om')] = 0.25
replace_cost[(u'ą', u'on')] = 0.25
replace_cost[(u'au', u'ał')] = 0.25

for (a, b) in replace_cost.keys():
    replace_cost[(b, a)] = replace_cost[(a, b)]


def cost(before, after):
    return replace_cost.get((before, after), max(len(before), len(after)))


def levenshtein(word_a, word_b):
    if len(word_a) < len(word_b):
        return levenshtein(word_b, word_a)

    if len(word_b) == 0:
        return len(word_a)

    p_previous_row = xrange(len(word_b) + 1)
    previous_row = xrange(len(word_b) + 1)
    for i, c1 in enumerate(word_a):
        current_row = [i + 1]
        for j, c2 in enumerate(word_b):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2) * cost(c1, c2)
            best = min(insertions, deletions, substitutions)

            if i > 0:
                subs12 = p_previous_row[j] + cost(word_a[i-1] + word_a[i], word_b[j])
                best = min(best, subs12)

            if j > 0:
                subs21 = previous_row[j-1] + cost(word_a[i], word_b[j-1] + word_b[j])
                best = min(best, subs21)

            if i > 0 and j > 0:
                subs22 = p_previous_row[j-1] + cost(word_a[i-1]+word_a[i], word_b[j-1]+word_b[j])
                best = min(best, subs22)

            if i > 0 and j > 0 and c1 == word_b[j-1] and c2 == word_a[i-1]:
                transpositions = p_previous_row[j-1] + 0.5
                best = min(best, transpositions)

            current_row.append(best)

        p_previous_row = previous_row
        previous_row = current_row

    return previous_row[-1]


r22 = [u'au', u'ał']
r21 = [u'ch', u'em', u'en', u'om', u'on', u'rz']


def generate_levenshtein(word, alphabet):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    inserts = [(a + c + b, 1) for a, b in splits for c in alphabet]
    deletes = [(a + b[1:], 1) for a, b in splits if b]
    replaces = [(a + c + b[1:], cost(b[0], c)) for a, b in splits for c in alphabet if b]
    replaces22 = [(a + c + b[2:], cost(b[:2], c)) for a, b in splits for c in r22 if len(b) > 1]
    replaces21 = [(a + c + b[1:], cost(b[:1], c)) for a, b in splits for c in r21 if b]
    transposes = [(a + b[1] + b[0] + b[2:], 0.5) for a, b in splits if len(b) > 1]

    return set(replaces22 + replaces21 + inserts + deletes + replaces + transposes)


def load_dictionary():
    with open(DICTIONARY_PATH) as f:
        lines = f.read().splitlines()
        split = map(lambda x: x.split(", "), lines)
        return chain.from_iterable(split)



with open('bledy.txt') as f:
    lines = f.read().splitlines()
    split = map(lambda x: x.decode('utf-8').split(" - "), lines)

errors = []
for pair in split:
    if len(pair) > 1:
        errors.append(levenshtein(pair[0], pair[1]))

NERRS = train(errors)

print NERRS

def main():
    dictionary = set(map(lambda word: word.decode('utf-8'), load_dictionary()))

    for word in fileinput.input():
        word = word.strip()
        word = word.decode("utf-8")
        proposals = propose3(word, dictionary)
        print u', '.join(proposals).encode("utf-8")


def best(tuples):
    yield tuples[0][0]

    for i in xrange(1, min(len(tuples), 5)):
        if tuples[0][1] == tuples[i][1]:
            yield tuples[i][0]
        else:
            break


def propose3(mistake, dictionary):
    alphabet = u'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź'

    words1 = ((word, dist) for (word, dist) in generate_levenshtein(mistake, alphabet))
    known1 = set((word, dist) for (word, dist) in generate_levenshtein(mistake, alphabet) if word in dictionary)

    if known1:
        ordered = sorted(known1, key=lambda x: x[1])
        return best(ordered)

    known2 = set((word2, dist1 + dist2) for (word1, dist1) in words1 for (word2, dist2) in
                 generate_levenshtein(word1, alphabet) if word2 in dictionary)

    if known2:
        ordered = sorted(known2.union(known1), key=lambda x: x[1])
        return best(ordered)

    return [mistake]


if __name__ == "__main__":
    main()