#!/usr/bin/env python

import fileinput


def main():

    words = [line.decode('utf-8').strip() for line in fileinput.input()]

    with open('atergo1700.pickled') as atergo_file:
        a_tergo = pickle.load(atergo_file)


if __name__ == '__main__':
    main()
