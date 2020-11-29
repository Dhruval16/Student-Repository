"""
Created on Sun Nov 29 14:20:10 2020
@author: Dhruval
"""

import os
import sqlite3
from flask import Flask, render_template, redirect
from typing import Dict

"""Build a Flask Python Appplication to display the student\
   grades prettytable from HW11 as a web page"""

app: Flask = Flask(__name__)


@app.route('/')
def index() -> str:
    """Redirect index to stevens_repository page"""
    return redirect('/stevens_repository')


@app.route('/stevens_repository')
def student_summary() -> str:
    """ Query for result table """
    db_path: str = "hw11.db"

    try:
        db: sqlite3.Connection = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        return f'Error: Unable to open database at path {db_path}'
    else:
        query: str = "select students.Name, students.CWID, grades.Course, \
            grades.Grade, instructors.Name from students,grades,instructors \
            where students.CWID=StudentCWID and \
                InstructorCWID=instructors.CWID \
            order by students.Name"
        data: Dict[str, str] = \
            [{'Name': name, 'CWID': cwid, 'Course': course, 'Grade': grade,
              'Instructor': instructor}
             for name, cwid, course, grade, instructor in db.execute(query)]

        db.close()

        return render_template(
            'stevens_repository.html',
            title='Stevens Repository',
            table_title='Student, Course, Grade, and Instructor',
            students=data)


app.run(debug=True)
