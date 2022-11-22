import os
import unittest

from pyhb.utils import user_path


class TestWords(unittest.TestCase):
    def test_user_path(self):
        """
        Make sure that user path is being calculated correctly

        :return: None
        """
        self.assertEqual(user_path,
                         os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").replace("tests", "pyhb"))

    def test_words(self):
        """
        Make sure that the words full fill certain criteria
        1) Word length is in the range of 2-6 inclusive.
        2) Word does not have any punctuation
        :return: None
        """

        with open(user_path + "/typing_tester/words.txt") as f:
            for word in f:
                word = word.strip()
                self.assertLessEqual(len(word), 6)
                self.assertGreaterEqual(len(word), 2)
                self.assertTrue(word.isalpha())


if __name__ == '__main__':
    unittest.main()
