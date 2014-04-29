#/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bartłomiej Szczepanik'

import fileinput


DELIMITER = "#####"


def main():
    print DELIMITER

    for word in fileinput.input():
        word = word.strip()

        print word


if __name__ == "__main__":
    main()
