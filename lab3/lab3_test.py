from unittest import TestCase
import lab3

__author__ = 'mequrel'


# class Lab3Test(TestCase):
#     def test_should_return_string_length_for_the_same_strings(self):
#         result = lab3.lcs_length("abcde", "abcde")
#         expected = 5
#
#         self.assertEquals(expected, result)

class PreprocessingTest(TestCase):
    def test_should_preprocess_data(self):
        strings = ["a@", "b@"]
        filter_func = lambda s: s.strip("@")

        expected_strings = ["a", "b"]

        filtered_strings, _ = lab3.preprocess(strings, filter_func)

        self.assertItemsEqual(expected_strings, filtered_strings)

    def test_should_reassemble_original_data(self):
        strings = ["a@", "b#", "c#", "d@"]
        filter_func = lambda s: s[:1]

        _, mapping = lab3.preprocess(strings, filter_func)

        clusters = [{"a", "b"}, {"c", "d"}]
        expected_clusters = [{"a@", "b#"}, {"c#", "d@"}]

        result_clusters = lab3.get_back_to_original_lines(clusters, mapping)

        self.assertItemsEqual(expected_clusters, result_clusters)


class LCSLengthTest(TestCase):
    def test_should_be_zero_if_nothing_in_common(self):
        result = lab3.lcs_length("abcde", "uwxyz")
        expected = 0

        self.assertEquals(expected, result)

    def test_should_be_string_length_for_the_same_strings(self):
        result = lab3.lcs_length("abcde", "abcde")
        expected = 5

        self.assertEquals(expected, result)

    def test_should_have_real_lcs_length(self):
        result = lab3.lcs_length("Bartek", "warta")
        expected = 3

        self.assertEquals(expected, result)

    def test_should_pick_the_longest_one(self):
        result = lab3.lcs_length("abc#abcd#abcde#abcdef", "abcdef@abcde@abcd@abc")
        expected = 6

        self.assertEquals(expected, result)


class SimilarityTest(TestCase):
    def test_should_be_similar_if_lcs_metric_is_high(self):
        self.assertTrue(lab3.similarity_func("abcdDEFGHIJKL", "xyzeDEFGHIJKL"))

    def test_should_not_be_similar_if_lsc_metric_is_low(self):
        self.assertFalse(lab3.similarity_func("abcdefghijkl", "klmnopqrstuvwxyz"))


class ClusterizeTest(TestCase):
    def test_should_gather_all_strings_with_metric_below_epsilon_in_one_cluster(self):
        # given
        strings = ["a", "b", "c", "d"]

        expected_clusters = [{"a", "b"}, {"c", "d"}]
        similarity_func = self.__similarity_func_from_clusters(expected_clusters)

        #when
        results = lab3.clusterize(strings, similarity_func)

        #then
        self.assertItemsEqual(expected_clusters, results)

    def test_should_return_zero_clusters_for_empty_strings(self):
        # given
        strings = []

        expected_clusters = []
        similarity_func = self.__similarity_func_from_clusters(expected_clusters)

        #when
        results = lab3.clusterize(strings, similarity_func)

        #then
        self.assertItemsEqual(expected_clusters, results)

    def __similarity_func_from_clusters(self, clusters):
        def similarity(string1, string2):
            return any([cluster for cluster in clusters if
                        {string1, string2}.intersection(cluster) == {string1, string2}])

        return similarity

    # def __metric_func_from_distances(self, distances):
    #     return lambda string1, string2: distances[(string1, string2)] \
    #         if (string1, string2) in distances else distances[(string2, string1)]
