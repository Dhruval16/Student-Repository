"""
Created on Sun Nov 15 07:40:33 2020
@author: Dhruval
"""

from prettytable import PrettyTable
from collections import defaultdict
from HW08_Dhruval_Thakkar import file_reader
import os


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
                    file_reader(path, 3, sep=';', header=True):
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
            for cwid, name, dept in file_reader(path, 3, sep='|', header=True):
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
                    file_reader(path, 4, sep='|', header=True):
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
