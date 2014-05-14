#!/usr/bin/env python

import fileinput
import pickle
from words import extract_words
from stemming import stem
from collections import Counter


RESULT_FILE_PREFIX = 'result'


def median(frequencies):
    all_counts = sum(map(lambda (_, count): count, frequencies))
    median_count_sum = all_counts // 2

    for rank, (word, count) in enumerate(frequencies):
        median_count_sum -= count

        if median_count_sum <= 0:
            return rank


def main():
    #with open('atergo_all.pickled') as atergo_file:
    #    a_tergo = pickle.load(atergo_file)

    words = extract_words(fileinput.input())
    #words = [stem(a_tergo, word) for word in words]

    frequencies = Counter(words).most_common()

    with open(RESULT_FILE_PREFIX + '.txt', 'w') as result_file:
        for rank, (word, count) in enumerate(frequencies):
            result_file.write("{0} {1} {2}\n".format(rank+1, count, word.encode('utf-8')))

    with open(RESULT_FILE_PREFIX + '-median.txt', 'w') as median_file:
        median_file.write(str(median(frequencies)))


if __name__ == '__main__':
    main()
