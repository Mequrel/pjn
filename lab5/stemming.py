__author__ = 'mequrel'

from collections import Counter
import pickle
import re


def _most_common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]


def _prefixes(word):
    for i in xrange(3, len(word)):
        yield word[:i]


def _to_value(bytes):
    return pickle.loads(bytes)


def _find_best_match(a_tergo, word):
    for prefix in reversed(list(_prefixes(word))):
        matching_items = a_tergo.items(prefix)

        if matching_items:
            values = map(lambda x: _to_value(x[1]), matching_items)
            return _most_common(values)

    return u'', u''


def stem(a_tergo, word):
    match = _find_best_match(a_tergo, word[::-1])
    return re.sub(match[0] + '$', match[1], word)