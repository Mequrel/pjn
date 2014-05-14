#!/usr/bin/env python

import fileinput
import pickle
from words import extract_words
from stemming import stem


def main():
    words = extract_words(fileinput.input())

    with open('atergo_all.pickled') as atergo_file:
        a_tergo = pickle.load(atergo_file)

    for word in list(words)[:100]:
        print stem(a_tergo, word), " ", word
        # add plp





if __name__ == '__main__':
    main()
