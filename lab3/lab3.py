#/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bartłomiej Szczepanik'

import fileinput


DELIMITER = "#####"


# def lcs_length(string1, string2):
#     return len(string1)


EPSILON = 0.2


def partition(l, p):
    return reduce(lambda x, y: x[0].append(y) or x if p(y) else x[1].append(y) or x, l, ([], []))


def clusterize(strings, metric_func):
    clusters = []

    while strings:
        head, tail = strings[0], strings[1:]
        similar, not_similar = partition(tail, lambda x: metric_func(x, head))
        cluster = set(similar + [head])
        clusters.append(cluster)
        strings = not_similar

    return clusters


def print_cluster(cluster):
    print DELIMITER

    for string in cluster:
        print string

    print ""


def lcs_length(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest = 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
            else:
                m[x][y] = 0

    return longest


def similarity_func(string1, string2):
    lcs_metric = 1 - lcs_length(string1, string2) / float(max(len(string1), len(string2)))
    return lcs_metric < 0.4


def main():
    lines = [line.strip() for line in fileinput.input()]

    clusters = clusterize(lines, similarity_func)

    for cluster in clusters:
        print_cluster(cluster)


if __name__ == "__main__":
    main()
