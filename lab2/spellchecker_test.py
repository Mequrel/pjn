#!/usr/bin/env python

import unittest
from spellchecker import propose


class ProposalsTestCase(unittest.TestCase):
    def test_should_return_the_same_word(self):
        self.assertEqual("angarzuje", propose("angarzuje"))

# add file reading test