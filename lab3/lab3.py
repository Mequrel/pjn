#/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bartłomiej Szczepanik'

import fileinput
import re
from collections import defaultdict
from itertools import chain

DELIMITER = "#####"


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
        #print cluster

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


def dice_coefficient(a, b):
    """dice coefficient 2nt/na + nb."""
    if not len(a) or not len(b): return 0.0
    if len(a) == 1:  a=a+u'.'
    if len(b) == 1:  b=b+u'.'

    a_bigram_list=[]
    for i in range(len(a)-1):
      a_bigram_list.append(a[i:i+2])
    b_bigram_list=[]
    for i in range(len(b)-1):
      b_bigram_list.append(b[i:i+2])

    a_bigrams = set(a_bigram_list)
    b_bigrams = set(b_bigram_list)
    overlap = len(a_bigrams & b_bigrams)
    dice_coeff = overlap * 2.0/(len(a_bigrams) + len(b_bigrams))
    return dice_coeff


def lcs_metric(string1, string2):
    return lcs_length(string1, string2) / float(max(len(string1), len(string2)))


def similarity_func(string1, string2):
    lcs = lcs_metric(string1[:8], string2[:8])
    dice = dice_coefficient(string1, string2)

    return (lcs + dice)/2 > 0.7


FREQUENT_SHORTCUTS = ['co.', 's.a.', ' sa ', ' co ']
FREQUENT_WORDS = ['fax', 'tel', 'llc', 'zip', 'ooo', '000', 'email', 'spzoo', 'ltd', 'spolkaakcyjna', 'spolka', 'company']
FREQUENT_WORDS += ['sanktpetersburg' 'saintpetersburg', 'stpetersburg', 'russia', 'poland', 'polska', 'moscow',
                   'denmark', 'hongkong', 'qingdao', 'shenzen', 'shanghai']


def filter_func(line):
    line = line.lower()

    for shortcut in FREQUENT_SHORTCUTS:
        line = line.replace(shortcut, "")

    line = re.sub("\W", "", line)
    line = re.sub("\d", "", line)
    for word in FREQUENT_WORDS:
        line = line.replace(word, "")


    return line


def preprocess(lines, filter_func):
    mapping = defaultdict(list)

    for line in lines:
        mapping[filter_func(line)].append(line)

    return map(filter_func, lines), mapping


def get_back_to_original_lines(clusters, mapping):
    def flatten(l):
        return list(chain.from_iterable(l))

    def get_back(cluster):
        return set(flatten([mapping[string] for string in cluster]))

    return [get_back(cluster) for cluster in clusters]


def main():
    lines = [line.strip() for line in fileinput.input()]
    filtered_lines, mapping = preprocess(lines, filter_func)

    clusters = clusterize(filtered_lines, similarity_func)

    clusters = get_back_to_original_lines(clusters, mapping)
    for cluster in clusters:
        print_cluster(cluster)


if __name__ == "__main__":
    main()
