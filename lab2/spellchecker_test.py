#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from spellchecker import propose
from spellchecker import levenshtein
from spellchecker import generate_levenshtein
from spellchecker import known_words


class ProposalsTestCase(unittest.TestCase):
    def test_should_return_a_word_from_dict_that_is_the_closest_one(self):
        dictionary = ("mangal", "angażuje", "aasdfasdf")

        expected = ["angażuje"]
        result = propose("angarzuje", dictionary)

        self.assertItemsEqual(expected, result)

    def test_should_return_all_words_with_the_same_distance(self):
        dictionary = ("barbarka", "barbar", "karbara", "xxx")

        expected = ["barbarka", "barbar", "karbara"]
        result = propose("barbara", dictionary)

        self.assertItemsEqual(expected, result)

    def test_should_return_once_doubled_word_in_dictionary(self):
        dictionary = ("angażuje", "angażuje", "aasdfasdf")

        expected = ["angażuje"]
        result = propose("angarzuje", dictionary)

        self.assertEqual(expected, result)


class LevenshteinDistanceTestCase(unittest.TestCase):
    def test_should_return_zero_for_the_same_words(self):
        self.assertEqual(0, levenshtein("mamusia", "mamusia"))

    def test_should_add_one_for_one_substitution(self):
        self.assertEqual(1, levenshtein("macusia", "mamusia"))

    def test_should_add_one_for_one_insertion(self):
        self.assertEqual(1, levenshtein("mamusika", "mamusia"))

    def test_should_add_one_for_one_deletion(self):
        self.assertEqual(1, levenshtein("mamusia", "mamusi"))

    def test_should_work_for_more_complicated_example(self):
        self.assertEqual(3, levenshtein("kitten", "sitting"))

    def test_should_count_half_for_transposition(self):
        self.assertEqual(0.5, levenshtein("mamusia", "maumsia"))


class LevenshteinGeneratorTestCase(unittest.TestCase):
    def test_should_generate_all_inserts(self):
        alphabet = "ab"

        result = generate_levenshtein("kot", alphabet)

        self.assertIn(("akot", 1), result)
        self.assertIn(("kaot", 1), result)
        self.assertIn(("koat", 1), result)
        self.assertIn(("kota", 1), result)
        self.assertIn(("bkot", 1), result)
        self.assertIn(("kbot", 1), result)
        self.assertIn(("kobt", 1), result)
        self.assertIn(("kotb", 1), result)

    def test_should_generate_all_deletes(self):
        alphabet = "ab"

        result = generate_levenshtein("kotek", alphabet)

        self.assertIn(("otek", 1), result)
        self.assertIn(("ktek", 1), result)
        self.assertIn(("koek", 1), result)
        self.assertIn(("kotk", 1), result)
        self.assertIn(("kote", 1), result)

    def test_should_generate_all_deletes2(self):
        alphabet = "ab"

        result = generate_levenshtein(u"uła", alphabet)

        self.assertIn((u"ła", 1), result)
        self.assertIn((u"ua", 1), result)
        self.assertIn((u"uł", 1), result)

    def test_should_generate_all_replaces(self):
        alphabet = "ab"

        result = generate_levenshtein("kot", alphabet)

        self.assertIn(("aot", 1), result)
        self.assertIn(("kat", 1), result)
        self.assertIn(("koa", 1), result)
        self.assertIn(("bot", 1), result)
        self.assertIn(("kbt", 1), result)
        self.assertIn(("kob", 1), result)

    def test_should_generate_all_transposes(self):
        alphabet = "ab"

        result = generate_levenshtein("kotek", alphabet)

        self.assertIn(("oktek", 0.5), result)
        self.assertIn(("ktoek", 0.5), result)
        self.assertIn(("koetk", 0.5), result)
        self.assertIn(("kotke", 0.5), result)
    #
    # def test_should_generate_the_same_word(self):
    #     alphabet = "ab"
    #
    #     result = generate_levenshtein("kotek", alphabet)
    #
    #     self.assertIn(("kotek", 0), result)

    def test_should_replace22(self):
        alphabet = ""
        print "Hello"
        result = generate_levenshtein(u"ałkcja", alphabet)

        self.assertIn((u"aukcja", 0.25), result)

    def test_a_bug(self):
        alphabet = u'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź'

        result = generate_levenshtein(u"abonamet", alphabet)

        self.assertIn((u"abonament", 1), result)

    def test_a_bug2(self):
        alphabet = u'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź'

        result = generate_levenshtein(u"automatow", alphabet)

        self.assertIn((u"automatów", 0.25), result)


class KnownWords(unittest.TestCase):
    def test_should_filter_known_words(self):
        dictionary = {"ala", "ola", "basia"}

        words = {"xxyy", "ala", "abc", "basia"}
        expected_known_words = ["ala", "basia"]

        result = known_words(words, dictionary)

        self.assertItemsEqual(expected_known_words, result)