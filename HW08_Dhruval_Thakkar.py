"""
Created on Fri Nov 06 08:20:33 2020
@author: Dhruval
"""

from typing import Tuple, Iterator, List, IO
from datetime import datetime, timedelta
import os
from prettytable import PrettyTable


def date_arithmetic() -> Tuple[datetime, datetime, int]:
    """ This function returns a tuple with two datetime object
        with date after 3 days of 02/27/2020, 3 days after
        02/27/2020 and interger value of difference of dates
        between 02/01/2019 and 09/30/2019 """
    three_days_after_02272020: datetime = datetime(
        2020, 2, 27).__add__(timedelta(3)).date()
    three_days_after_02272019: datetime = datetime(
        2019, 2, 27).__add__(timedelta(3)).date()
    days_passed_02012019_09302019: int = (datetime(2019, 9, 30)
                                          - datetime(2019, 2, 1)).days
    return three_days_after_02272020, three_days_after_02272019, \
        int(days_passed_02012019_09302019)


def file_reader(path: str, fields: int, sep: str = ",",
                header: bool = False) -> Iterator[List[str]]:
    """ This function returns an iterator string list which is
        produced by reading text files with fixed number of fields
        If the number of fields in any line mismatches the expected
        number of fields we will recieve an error """
    file_name: str = path
    try:
        fp: IO = open(file_name, 'r')
    except FileNotFoundError:
        print(f"Can't open {file_name}")
    else:
        with fp:
            count: int = 0
            if header:
                next(fp)
            while True:
                count = count + 1
                try:
                    line_next: str = next(fp)
                except Exception:
                    break
                line_next = line_next.split(sep)
                line_next[len(
                    line_next)-1] = line_next[len(
                        line_next)-1][:len(line_next[len(line_next)-1])-1]
                if len(line_next) != fields:
                    raise ValueError(
                        f"{file_name} has {len(line_next)} fields on the line\
                            {count} but expected {fields}")

                yield line_next


class FileAnalyzer:
    """ This class searches given directory for Python files. Also for each .py
        file it will open each file and calculate summary of following data:
        - the file name
        - the total number of lines in the file
        - the total number of characters in the file
        - the number of Python functions(lines starting with 'def')
        - the number of python classes(lines starting with 'class)
    """

    def __init__(self, directory: str):
        """
            This function will initialize the directory valriable with given
            directory and also calls files_summary and analyse_files functions
        """
        self.directory: str = directory
        self.files_summary: Dict[str, Dict[str, int]] = dict()
        self.analyse_files()

    def analyse_files(self) -> None:
        """
            This function will populate the summerized data into self.files_
            summary()
        """
        file_name: str = os.listdir(self.directory)
        for fn in file_name:
            class_cnt: int = 0
            function_cnt: int = 0
            line_cnt: int = 0
            char_cnt: int = 0
            if fn.endswith(".py"):
                try:
                    fp: IO = open(fn, 'r')
                except FileNotFoundError:
                    print(f"Can't open {file_name}")
                else:
                    with fp:
                        while True:
                            try:
                                line_next: str = next(fp)
                            except Exception:
                                break
                            line_cnt = line_cnt + 1
                            char_cnt = char_cnt + len(line_next)
                            if line_next.startswith('class '):
                                class_cnt = class_cnt + 1
                            elif line_next.lstrip().startswith('def '):
                                function_cnt = function_cnt + 1
                self.files_summary[os.path.join(self.directory, fn)] = \
                    {
                        'class': class_cnt,
                        'function': function_cnt,
                        'line': line_cnt,
                        'char': char_cnt
                }

    def pretty_print(self) -> None:
        """
            This function will print out the pretty table from the data stored
            in the self.files_summary.
        """
        pt: PrettyTable = PrettyTable(field_names=["File Name", "Classes",
                                                   "Functions", "Lines",
                                                   "Characters"])
        for File_Name in self.files_summary:
            new_dict = self.files_summary[File_Name]
            pt.add_row([File_Name, new_dict['class'],
                        new_dict['function'],
                        new_dict['line'],
                        new_dict['char']])

        print(pt)
