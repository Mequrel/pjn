#!/usr/bin/env python

import fileinput


def main():
    for word in fileinput.input():
        print propose(word)


def propose(word):
    return word

if __name__ == "__main__":
    main()