#!/usr/bin/env python

import fileinput
from plp import PLP


def main():
    words = [line.decode('utf-8').strip() for line in fileinput.input()]

    p = PLP()

    for word in words:
        stemmed_word = word

        rec_list = p.rec(word)
        if rec_list:
            stemmed_word = p.bform(rec_list[0])

        print "{0},{1}".format(word.encode("utf-8"), stemmed_word.encode("utf-8"))

if __name__ == '__main__':
    main()
