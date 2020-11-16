"""
Created on Fri Nov 06 08:20:33 2020

@author: Dhruval
"""

import unittest
from HW08_Dhruval_Thakkar import date_arithmetic, file_reader
from HW08_Dhruval_Thakkar import FileAnalyzer
from datetime import datetime


class DateArithmeticTest(unittest.TestCase):
    """ This function checks test case for date_arithmetic function
    """

    def test_date_arithmetic(self):
        self.assertEqual(date_arithmetic(), (datetime(2020, 3, 1).date(),
                                             datetime(2019, 3, 2).date(), 241))


class FileReaderTest(unittest.TestCase):
    """ This function checks test case for file_reader function
    """

    def test_file_reader(self):

        str1: str = list(file_reader('hello.txt', 3, '|', True))
        str2: str = [['123', 'Jin He', 'Computer Science\n'],
                     ['234', 'Nanda Koka', 'Software Engineering\n'],
                     ['345', 'Benji Cai', 'Software Engineering']]

        self.assertEqual(str1, str2)
        with self.assertRaises(ValueError):
            list(file_reader('hello.txt', 2, '|', True))
        with self.assertRaises(FileNotFoundError):
            list(file_reader('123.txt', 3, '|', True))


class FileAnalyzerTest(unittest.TestCase):
    """ This function checks test case for file_analyzer class
    """

    def test_file_analyzer(self):
        str1: str = FileAnalyzer(
            'C:/Users/Dhruval/Desktop/Sem-3/SSW-810/Homework/hw')
        str2: str = {
            'C:/Users/Dhruval/Desktop/Sem-3/SSW-810/Homework/hw' +
            '\\0_defs_in_this_file.py':
            {'char': 57, 'class': 0, 'function': 0,
             'line': 3},
            'C:/Users/Dhruval/Desktop/Sem-3/SSW-810/Homework/hw\\file1.py':
                {'char': 270, 'class': 2, 'function': 4, 'line': 25
                 }}
        self.assertEqual(str1.files_summary, str2)
        with self.assertRaises(FileNotFoundError):
            FileAnalyzer(' ')


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
