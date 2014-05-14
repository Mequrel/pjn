#!/usr/bin/env python

import fileinput
import pickle
from words import extract_words
from stemming import stem
from collections import Counter


def main():
    with open('atergo_all.pickled') as atergo_file:
        a_tergo = pickle.load(atergo_file)

    words = extract_words(fileinput.input())
    words = [stem(a_tergo, word) for word in words]

    frequencies = Counter(words).most_common()

    for word, count in frequencies:
        print("{} {}".format(count, word.encode('utf-8')))


if __name__ == '__main__':
    main()
