import re
import string
from itertools import chain

__author__ = 'mequrel'


_PUNCTUATION_REGEX = re.compile("[" + re.escape(string.punctuation) + "]")


def _extract_words_from_line(line):
    no_punctuation = re.sub(_PUNCTUATION_REGEX, "\n", line)
    lowered = no_punctuation.lower()
    return lowered.split()


def extract_words(input_file):
    return chain.from_iterable(_extract_words_from_line(line.decode('utf-8').strip()) for line in input_file)