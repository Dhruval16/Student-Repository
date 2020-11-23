"""
Created on Sun Nov 22 17:40:33 2020
@author: Dhruval
"""
import unittest
from prettytable import PrettyTable
from collections import defaultdict
from HW08_Dhruval_Thakkar import file_reader
import os
import sqlite3


class Major:
    """ This is a Major class which contains data from the majors.txt. """

    def __init__(self, major: str) -> None:
        """ Initializes the major, required and elective courses """
        self.major = major
        self.required_courses = set()
        self.elective_courses = set()

    def set_course_re(self, flag, course: str) -> None:
        """ Groups required or elective courses from the majors.txt file """
        if flag.lower() == 'e':
            self.elective_courses.add(course)
        elif flag.lower() == 'r':
            self.required_courses.add(course)
        else:
            raise ValueError(f"Unknown Flag: {flag}")

    def get_courses(self, courses):
        """ Checks for the grades in the list of grades and
            gives set of list of courses as output"""
        completed_courses = set()
        required_c = self.required_courses.copy()
        elective_c = self.elective_courses.copy()

        for course, grade in courses.items():
            if grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
                completed_courses.add(course)
                if course in self.elective_courses:
                    elective_c = []

            if course in self.required_courses and grade in\
                    ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
                required_c.remove(course)

        return completed_courses, required_c, elective_c

    def info(self):
        """ return a list of the information about the courses needed for \
            the pretty table"""
        return [self.major, sorted(self.required_courses),
                sorted(self.elective_courses)]


class Student:
    def __init__(self, CWID: str, name: str, major: str) -> None:
        self.CWID = CWID
        self.name = name
        self.major = major
        self.courses_taken: Dict[str, str] = dict()

        self.completed_courses = []
        self.remaining_required = []
        self.remaining_electives = []

    def gpa(self) -> float:
        """calculate the GPA and return to student class"""
        grades: Dict[str, float] = {"A": 4.00, "A-": 3.75, "B+": 3.25,
                                    "B": 3.00, "B-": 2.75, "C+": 2.25,
                                    "C": 2.00, "C-": 0.00, "D+": 0.00,
                                    "D": 0.00, "D-": 0.00, "F": 0.00}
        try:
            return round(sum(
                [grades[grade] for grade in
                 self.courses_taken.values()]) /
                len(self.courses_taken.values()), 2)
        except ZeroDivisionError as e:
            print("Divisor can not be zero")

    def add_course_grade(self, course: str, grade: str):
        """ This fucntion will add courses and obtained grades in dictionary"""
        self.courses_taken[course] = grade

    def course_remaining(self, major):
        """ This function will see for the courses in the major class by \
            calling the remaining courses of the major class. """
        self.completed_courses, self.remaining_required, \
            self.remaining_electives = major.get_courses(
                self.courses_taken)

    def get_student_info(self):
        """ Returns list of info about students """
        return [self.CWID, self.name, self.major,
                sorted(self.completed_courses),
                sorted(self.remaining_required),
                sorted(self.remaining_electives), self.gpa()]


class Instructor:
    """ This provides information of the instructor which includes CWID, \
        Name, Department, and the courses they teach This will return the \
             instructor information for the repository class. """

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        """ This is to initialize the cwid, name, department, and the courses\
            they teach in protected form. """
        self.cwid: str = cwid
        self.name: str = name
        self.dept: str = dept
        self.courses: DefaultDict[str, int] = defaultdict(int)

    def add_course_student(self, course: str) -> None:
        """ This funtion will add the number of courses taught by them """
        self.courses[course] += 1

    def get_instructor_info(self):
        """ return a list of the information about the instructor needed for\
            the pretty table """
        for course, student_num in self.courses.items():
            yield [self.cwid, self.name, self.dept, course, student_num]


class File_Reader:
    def __init__(self, path: str, ptable=False) -> None:
        """store all students, instructors, majors and print prettytables """
        if not os.path.exists(path):
            raise FileNotFoundError(f'{path} not found')
        self.path: str = path
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self._major: Dict[str, Major] = dict()
        try:
            self._read_major(os.path.join(path, "majors.txt"))
            self._read_students(os.path.join(path, "students.txt"))
            self._read_instructors(os.path.join(path, "instructors.txt"))
            self._read_grades(os.path.join(path, "grades.txt"))
            self._read_re()
        except (FileNotFoundError, ValueError) as e:
            print(e)

        if ptable:
            self.major_pretty_table()
            self.student_pretty_table()
            self.instructor_pretty_table()

    def _read_major(self, path: str) -> None:
        """ read each line from majors file and create instance of class major
        and if the file not found or any value error,\
             it raises an exception """
        try:
            for major, req, course in\
                    file_reader(path, 3, sep='\t', header=True):
                if major not in self._major:
                    self._major[major] = Major(major)

                self._major[major].set_course_re(req, course)

        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _read_students(self, path: str) -> None:
        """ read each line from student file and create instance of \
            class student and if the file not found or any value error\
            , it raises an exception """
        try:
            for cwid, name, major in \
                    file_reader(path, 3, sep='\t', header=True):
                if cwid not in self._students:
                    self._students[cwid] = Student(cwid, name, major)
                else:
                    print(f" Duplicate student {cwid}")
        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _read_instructors(self, path: str):
        """ read each line from instructors file and create instance\
            of class instructor and if the file not found or any\
            value error, it raises an exception"""
        try:
            for cwid, name, dept in file_reader(path, 3, sep='\t',
                                                header=True):
                if cwid not in self._instructors:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
                else:
                    print(f" Duplicate instructor {cwid}")

        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _read_grades(self, path: str) -> None:
        """ read the student_cwid, course, grade, instructor_cwid from the \
            grades file and checks for the individual student and the \
            individual instructor.Raises an exception when unknown student\
            is found"""
        try:
            for student_cwid, course, grade, instructor_cwid in \
                    file_reader(path, 4, sep='\t', header=True):
                try:
                    s: Student = self._students[student_cwid]
                    s.add_course_grade(course, grade)
                except KeyError:
                    print(f"Found grade for unknown student {student_cwid}")
                try:
                    inst: Instructor = self._instructors[instructor_cwid]
                    inst.add_course_student(course)
                except KeyError:
                    print(f"Found grade for unknown student {instructor_cwid}")
        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _read_re(self):
        """ checking for the cwid in the major\
            which is not in the repository """
        for cwid in self._students:
            student_info = self._students[cwid]
            student_major = student_info.major

            try:
                student_info.course_remaining(self._major[student_major])
            except Exception:
                print(
                    f" Student with CWID {cwid}  has a major\
                         {student_major} not in repository")

    def major_pretty_table(self) -> None:
        """ print pretty table with major information by calling the\
            global constant."""
        pt = PrettyTable(field_names=["Major", "Required", "Electives"])
        for mj in self._major.values():
            pt.add_row(mj.info())

        print("Major Summary")
        print(pt)

    def student_pretty_table(self) -> None:
        """ print pretty table with student information by calling the\
            global constant."""
        pt = PrettyTable(field_names=[
                         'CWID', 'Name', 'Major', 'Completed Courses',
                         'Remaining Required', 'Remaining Electives', 'GPA'])
        for stu in self._students.values():
            pt.add_row(stu.get_student_info())

        print("Student Summary")
        print(pt)

    def instructor_pretty_table(self) -> None:
        """ print pretty table with instructor information by calling the \
            global constant."""
        pt = PrettyTable(field_names=["CWID", "Name", "Dept", "Courses",
                                      "Students"])
        for stu in self._instructors.values():
            for row in stu.get_instructor_info():
                pt.add_row(row)

        print("Instructor Summary")
        print(pt)

    def student_grades_table_db(self, db_path) -> None:
        """ print pretty table with query result, which uses students,\
            grades and instructors table. """
        pt = PrettyTable(field_names=["Name", "CWID", "Course", "Grade",
                                      "Instructor"])
        db_file: str = db_path
        db: sqlite3.Connection = sqlite3.connect(db_file)
        for row in db.execute("select s.Name as Student, s.CWID, g.Course,\
            g.Grade, i.Name as Instructor from grades g, \
            students s, instructors i where g.StudentCWID=s.CWID \
                and g.InstructorCWID=i.CWID"):
            pt.add_row(row)

        print("Student Grade Summary")
        print(pt)


def main():
    """ Put directory address in File_Reader() """
    f: File_Reader = File_Reader(
        "C:/Users/Dhruval/Desktop/Student-Repository")
    f.major_pretty_table()
    f.student_pretty_table()
    f.instructor_pretty_table()
    f.student_grades_table_db("C:/Users/Dhruval/Desktop/Sem-3/SSW-810/hw11.db")


class TestSetUp(unittest.TestCase):
    def test_setup(self) -> None:
        self.file_r: File_Reader = File_Reader(
            "C:/Users/Dhruval/Desktop/Sem-3/SSW-810/Homework/HW_11", False)


class TestMajor(unittest.TestCase):
    def test_majorclass(self) -> None:
        self.file_r: File_Reader = File_Reader(
            "C:/Users/Dhruval/Desktop/Sem-3/SSW-810/Homework/HW_11", False)
        print([major.info() for major in
               self.file_r._major.values()])
        self.assertEqual([['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'],
                           ['CS 501', 'CS 546']],
                          ['CS', ['CS 546', 'CS 570'],
                           ['SSW 565', 'SSW 810']]],
                         [major.info() for major in
                             self.file_r._major.values()])


class TestInstructor(unittest.TestCase):
    def test_instructorclass(self) -> None:
        self.file_r: File_Reader = File_Reader(
            "C:/Users/Dhruval/Desktop/Sem-3/SSW-810/Homework/HW_11", False)
        self.assertEqual([['98764', 'Cohen, R', 'SFEN', 'CS 546', 1],
                          ['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4],
                          ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1],
                          ['98762', 'Hawking, S', 'CS', 'CS 501', 1],
                          ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
                          ['98762', 'Hawking, S', 'CS', 'CS 570', 1]],
                         [list(val) for instructor in
                             self.file_r._instructors.values(
                         ) for val in instructor.get_instructor_info()])


class TestStudentGrade(unittest.TestCase):
    def test_student_grade_info(self) -> None:
        self.file_r: File_Reader = File_Reader(
            "C:/Users/Dhruval/Desktop/Sem-3/SSW-810/Homework/HW_11", False)
        result = []
        db = sqlite3.connect(
            "C:/Users/Dhruval/Desktop/Sem-3/SSW-810/hw11.db")
        for row in db.execute("select students.Name, students.CWID, \
            grades.Course, grades.Grade, instructors.Name from students,\
                grades,instructors where students.CWID=StudentCWID and\
                     InstructorCWID=instructors.CWID order by students.Name"):
            result.append(row)
            self.assertEqual
            ([('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
              ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
              ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
              ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
              ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
              ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
              ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
              ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
              ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')], result)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
    main()
