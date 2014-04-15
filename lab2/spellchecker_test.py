#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from spellchecker import propose
from spellchecker import levenshtein

class ProposalsTestCase(unittest.TestCase):
    def test_should_return_a_word_from_dict_that_is_the_closest_one(self):
        dictionary = ("mangal", "angażuje", "aasdfasdf")
        self.assertEqual("angażuje", propose("angarzuje", dictionary))

class LevenshteinDistanceTestCase(unittest.TestCase):
    def test_should_return_zero_for_the_same_words(self):
        self.assertEqual(0, levenshtein("mamusia", "mamusia"))

    def test_should_add_one_for_one_substitution(self):
        self.assertEqual(1, levenshtein("macusia", "mamusia"))

    def test_should_add_one_for_one_insertion(self):
        self.assertEqual(1, levenshtein("mamusika", "mamusia"))

    def test_should_add_one_for_one_deletion(self):
        self.assertEqual(1, levenshtein("mamusia", "mamusi"))

    def test_should_word_for_more_complicated_example(self):
        self.assertEqual(3, levenshtein("kitten", "sitting"))