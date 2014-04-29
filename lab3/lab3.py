#/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bartłomiej Szczepanik'

import fileinput


DELIMITER = "#####"


def clusterize(strings):
    return [strings]


def print_cluster(cluster):
    print DELIMITER

    for string in cluster:
        print string

    print ""


def main():
    lines = [line.strip() for line in fileinput.input()]

    clusters = clusterize(lines)

    for cluster in clusters:
        print_cluster(cluster)


if __name__ == "__main__":
    main()
