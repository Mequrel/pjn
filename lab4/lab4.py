#!/usr/bin/env python

import fileinput


def main():
    words = [line.strip() for line in fileinput.input()]

    for word in words:
        print "{0},{1}".format(word, word)

if __name__ == '__main__':
    main()
