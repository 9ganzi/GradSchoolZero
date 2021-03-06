import sqlite3
from pandas.core.indexing import _IndexSlice
from datetime import datetime


# import task5
import display_db
import sys
import csv
import os
from user import Registrar, Student, Instructor, User
import random
import string
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableView,
    QPushButton,
    QComboBox,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QCursor, QRegExpValidator, QStandardItem
from functools import partial  # Aiman 11/6


name = ""
email = ""
acc_type = ""
id = ""
loginState = ""  # Aiman
user = None

class_set_up = 0
course_registration = 1
class_running = 2
grading = 3

# Aiman Start

comboBox_stylesheet = (
    "QComboBox{color:black;background-color:white;border-radius:10;"
    "border: 2px solid #076DF2}"
    "QComboBox:focus{box-shadow: 0 0 10px #076DF2;}"
    "QComboBox::drop-down { "
    "subcontrol-origin: padding;"
    "subcontrol-position: top right; "
    "border-left-color: white; "
    "border-left-style: solid; "
    "border-top-right-radius: 10px; "
    "border-bottom-right-radius: 10px; "
    "}"
    "QComboBox:on{border-bottom-right-radius:0;border-bottom-left-radius:0;"
    "border-bottom: 0px;}"
    "QComboBox QAbstractItemView {"
    "color:black;"
    "background:white;"
    "selection-background-color: #076DF2;"
    "selection-color: bl`ack;"
    "border: 2px solid #076DF2};"
    "border-top: 0px;"
)

instructors = [
    "William John",
    "Mike Chen",
    "Michael Brown",
    "Stephen William",
    "Ali Ahmet",
    "Jie Wei",
    "George Lucci",
    "Nancy Bishop",
    "Erik William",
    "Alison Jacob",
]

classes = [
    ["Csc 10300", "Fr 10:00am~12:15pm", "William John", "15"],
    ["Csc 10400", "MoWe 11:00am~12:15pm", "Mike Chen", "13"],
    ["Csc 21700", "MoWe 03:00pm~04:15pm", "Michael Brown", "10"],
    ["Csc 22100", "TuTh 09:00am~10:30pm", "Stephen William", "12"],
    ["Csc 30100", "TuTh 09:00am~10:15am", "Ali Ahmet", "15"],
    ["Csc 32200", "TuTh 06:00pm~07:15pm", "Jie Wei", "15"],
    ["Csc 47400", "MoWe 09:00am~10:15pm", "George Lucci", "10"],
    ["Csc 47200", "Fr 03:00pm~05:30pm", "Nancy Bishop", "12"],
    ["Csc 59866", "MoWe 01:00pm~02:15pm", "Erik William", "15"],
    ["Csc 59867", "TuTh 05:00pm~06:15pm", "Alison Jacob", "15"],
]

# Aiman end

# Display top 5 students with highest gpa
def display_honor_roll():
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    honor_students_join = c.execute(
        """SELECT first, last, gpa FROM users Inner Join students USING(user_id) ORDER BY gpa DESC LIMIT 5""",
    ).fetchall()
    result2 = []
    final_result = "Highest Rated Students: \n\n"
    for col in zip(*honor_students_join):
        result2.append(max([len(str(item)) for item in col]))
    format = "  ".join(["{:<" + str(l) + "}" for l in result2])
    for row in honor_students_join:
        final_result += format.format(*row)
        final_result += "\n"
    return final_result


def display_highest_classes():
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    honor_students_join = c.execute(
        """SELECT course_name, course_rating FROM courses WHERE course_rating IS NOT NULL ORDER BY course_rating DESC LIMIT 5""",
    ).fetchall()
    result2 = []
    final_result = "Highest Rated Courses: \n\n"
    for col in zip(*honor_students_join):
        result2.append(max([len(str(item)) for item in col]))
    format = "  ".join(["{:<" + str(l) + "}" for l in result2])
    for row in honor_students_join:
        final_result += format.format(*row)
        final_result += "\n"
    return final_result


def display_lowest_classes():
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    honor_students_join = c.execute(
        """SELECT course_name, course_rating FROM courses WHERE course_rating IS NOT NULL AND course_rating ORDER BY course_rating ASC LIMIT 5""",
    ).fetchall()
    result2 = []
    final_result = "Lowest Rated Courses: \n\n"
    for col in zip(*honor_students_join):
        result2.append(max([len(str(item)) for item in col]))
    format = "  ".join(["{:<" + str(l) + "}" for l in result2])
    for row in honor_students_join:
        final_result += format.format(*row)
        final_result += "\n"
    return final_result


def get_current_period():
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    curr_period = c.execute("Select current_period FROM periods ").fetchone()[0]
    conn.commit()
    conn.close()
    return curr_period


def go_next_period():
    next_period = (get_current_period() + 1) % 5
    print(next_period)
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    c.execute(
        """UPDATE periods SET current_period=:next_period""",
        {"next_period": next_period},
    )
    conn.commit()
    conn.close()


def issue_warning_instructor(instructor_id):
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    # get current warning_count
    c.execute(
        "SELECT warning_count From instructors where instructor_id = :instructor_id",
        {"instructor_id": instructor_id},
    )
    new_warning_count = (
        c.fetchone()[0] + 1
    )  # c.fetchone()[0] isolate variable from tuple
    # print(new_warning_count)
    # update student warning_count
    c.execute(
        """UPDATE instructors SET warning_count = :new_warning_count
                        WHERE instructor_id =:instructor_id""",
        {"instructor_id": instructor_id, "new_warning_count": new_warning_count},
    )
    conn.commit()
    conn.close()


class mainWindow(QMainWindow):
    # the innit function with main app attributes
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setWindowTitle("Collage App")
        self.setFixedSize(1260, 800)
        # -----------------------------------------#
        # self.mainpage_home_registrar()
        # -----------comment this line!!-----------#
        self.startup_page()

    # mike
    def apply_graduation_student(self):
        global user
        user.apply_graduation()
        self.mainpage_home_student()

    # Joel
    def add_review_page(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QHBoxLayout()
        # ----------------Design-----------------

        self.boxesW = QWidget()
        self.boxesL = QVBoxLayout()

        # self.nameTXT = QtWidgets.QLabel()
        # self.nameTXT.setText("Your Name :")
        # self.nameTXT.setStyleSheet("color:white;")
        # self.nameTXT.setFont(QFont("Times", 20))
        # self.boxesL.addWidget(self.nameTXT)

        # self.space = QWidget()
        # self.space.setFixedHeight(30)
        # self.boxesL.addWidget(self.space)

        # self.nameBOX = QtWidgets.QLineEdit()
        # self.nameBOX.setStyleSheet(
        #     "color:black;background-color:white;padding-left:20;border-radius:10px;"
        # )
        # self.nameBOX.setFont(QFont("Times", 20))
        # self.nameBOX.setFixedSize(600, 60)
        # self.boxesL.addWidget(self.nameBOX)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        """ self.emailTXT = QtWidgets.QLabel()
        self.emailTXT.setText("E-mail :")
        self.emailTXT.setStyleSheet("color:white;")
        self.emailTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.emailTXT)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.emailBOX = QtWidgets.QLineEdit()
        self.emailBOX.setStyleSheet("color:black;background-color:white;padding-left:20;border-radius:10px;")
        self.emailBOX.setFont(QFont("Century Gothic", 20))
        self.emailBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.emailBOX)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space) """

        self.studentidTXT = QtWidgets.QLabel()
        self.studentidTXT.setText("Your Student ID Number :")
        self.studentidTXT.setStyleSheet("color:white;")
        self.studentidTXT.setFont(QFont("Times", 20))
        self.boxesL.addWidget(self.studentidTXT)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.studentidBOX = QtWidgets.QLineEdit()
        self.studentidBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.studentidBOX.setFont(QFont("Times", 20))
        self.studentidBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.studentidBOX)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        # self.classtakingTXT = QtWidgets.QLabel()
        # self.classtakingTXT.setText("Class You're Taking :")
        # self.classtakingTXT.setStyleSheet("color:white;")
        # self.classtakingTXT.setFont(QFont("Century Gothic", 20))
        # self.boxesL.addWidget(self.classtakingTXT)

        # self.space = QWidget()
        # self.space.setFixedHeight(30)
        # self.boxesL.addWidget(self.space)

        # self.classtakingBOX = QtWidgets.QLineEdit()
        # self.classtakingBOX.setStyleSheet(
        #     "color:black;background-color:white;padding-left:20;border-radius:10px;"
        # )
        # self.classtakingBOX.setFont(QFont("Century Gothic", 20))
        # self.classtakingBOX.setFixedSize(600, 60)
        # self.boxesL.addWidget(self.classtakingBOX)

        self.courseidTXT = QtWidgets.QLabel()
        self.courseidTXT.setText("Your Course ID :")
        self.courseidTXT.setStyleSheet("color:white;")
        self.courseidTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.courseidTXT)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.courseidBOX = QtWidgets.QLineEdit()
        self.courseidBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.courseidBOX.setFont(QFont("Century Gothic", 20))
        self.courseidBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.courseidBOX)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        # self.profnameTXT = QtWidgets.QLabel()
        # self.profnameTXT.setText("Professor Name :")
        # self.profnameTXT.setStyleSheet("color:white;")
        # self.profnameTXT.setFont(QFont("Century Gothic", 20))
        # self.boxesL.addWidget(self.profnameTXT)

        # self.space = QWidget()
        # self.space.setFixedHeight(30)
        # self.boxesL.addWidget(self.space)

        # self.profnameBOX = QtWidgets.QLineEdit()
        # self.profnameBOX.setStyleSheet(
        #     "color:black;background-color:white;padding-left:20;border-radius:10px;"
        # )
        # self.profnameBOX.setFont(QFont("Century Gothic", 20))
        # self.profnameBOX.setFixedSize(600, 60)
        # self.boxesL.addWidget(self.profnameBOX)

        # self.space = QWidget()
        # self.space.setFixedHeight(30)
        # self.boxesL.addWidget(self.profnameBOX)

        self.ratingTXT = QtWidgets.QLabel()
        self.ratingTXT.setText("Your Class Rating (out of 5) :")
        self.ratingTXT.setStyleSheet("color:white;")
        self.ratingTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.ratingTXT)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.ratingBOX = QtWidgets.QLineEdit()
        self.ratingBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.ratingBOX.setFont(QFont("Century Gothic", 20))
        self.ratingBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.ratingBOX)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.reviewTXT = QtWidgets.QLabel()
        self.reviewTXT.setText("Your Review :")
        self.reviewTXT.setStyleSheet("color:white;")
        self.reviewTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.reviewTXT)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.reviewBOX = QtWidgets.QLineEdit()
        self.reviewBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.reviewBOX.setFont(QFont("Century Gothic", 20))
        self.reviewBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.reviewBOX)

        self.boxesW.setLayout(self.boxesL)
        self.mainL.addWidget(self.boxesW)
        self.mainW.setLayout(self.mainL)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.buttonsW = QWidget()
        self.buttonsL = QHBoxLayout()

        self.submitFBTN = QtWidgets.QPushButton()
        self.submitFBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.submitFBTN.setText("Submit Review")
        self.submitFBTN.setFont(QFont("Century Gothic", 20))
        self.submitFBTN.setFixedSize(180, 60)
        self.submitFBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.buttonsW = QWidget()
        self.buttonsL.addWidget(self.submitFBTN)

        self.space = QWidget()
        self.space.setFixedWidth(30)
        self.buttonsL.addWidget(self.space)

        self.backToMainBTN = QtWidgets.QPushButton()
        self.backToMainBTN.setText("Back")
        self.backToMainBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToMainBTN.setFont(QFont("Century Gothic", 20))
        self.backToMainBTN.setFixedSize(180, 60)
        self.backToMainBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.buttonsL.addWidget(self.backToMainBTN)
        self.buttonsW.setLayout(self.buttonsL)
        self.combo = QtWidgets.QComboBox()
        self.combo.setStyleSheet(
            "QComboBox{color:white;background-color:#076DF2;border-radius:10;"
            "margin-left:110px;padding-left:10px;}"
            "QComboBox::drop-down { "
            "subcontrol-origin: padding;"
            "subcontrol-position: top right; "
            "width: 15px; "
            "border-left-width: 1px; "
            "border-left-color: #076DF2; "
            "border-left-style: solid; "
            "border-top-right-radius: 10px; "
            "border-bottom-right-radius: 10px; "
            "}"
            "QComboBox:on{border-bottom-right-radius:0;border-bottom-left-radius:0;}"
            "QComboBox QAbstractItemView {"
            "background:#076DF2;"
            "selection-background-color: #03469e;}"
        )

        self.combo.setFont(QFont("Myriad Pro", 18))
        self.combo.setFixedSize(500, 50)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL.addWidget(self.combo)

        self.boxesL.addWidget(self.buttonsW)

        self.boxesW.setLayout(self.boxesL)
        self.mainL.addWidget(self.boxesW)
        self.mainW.setLayout(self.mainL)

        self.space = QWidget()
        self.space.setFixedWidth(180)

        self.mainL.addWidget(self.space)

        self.tipsW = QWidget()
        self.tipsL = QVBoxLayout()

        self.tipsW.setFixedSize(400, 600)
        self.tipsW.setStyleSheet("border: 1px solid white;border-radius: 10px;")

        self.tipsTXT = QtWidgets.QTextEdit()
        self.tipsTXT.setText(
            "\nA student who is in class can write reviews of this case and assign stars (1 worst to 5 best), which will be summarized in the class, no one else except the registrars know who rated which class. The instructor of any course receiving average rating <2 will be warned. An instructor who accumulated 3 warnings will be suspended. The student cannot rate the class after the instructor post the grade. Reviews with 1 or 2 taboo words (the list of taboo words are set up by registrars) will be shown but those words are changed to * and the author receives one warning; whereas reviews with >=3 taboo???s words are not shown in the systems and the author will receive 2 warnings."
        )

        self.tipsTXT.setFont(QFont("Century Gothic", 20))
        self.tipsTXT.setAlignment(Qt.AlignHCenter)
        self.tipsTXT.setStyleSheet("color:white;border:0;")

        self.tipsL.addWidget(self.tipsTXT)

        self.tipsW.setLayout(self.tipsL)
        self.mainL.addWidget(self.tipsW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked
        self.backToMainBTN.clicked.connect(self.mainpage_home_student)
        # self.submitBTN.clicked.connect(self.add_review_page)
        self.submitFBTN.clicked.connect(self.add_review)

    def add_review(self):
        # global id
        # global acc_type
        # global name
        # global email
        
        if get_current_period()== 4: # in post grading session, studenst cant do review
#             print("Its after grading season, cant post reviews")
            self.mainpage_home_student()
            return
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS reviews (
                review_id integer PRIMARY KEY,
                Rating text NOT NULL,
                student_id integer NOT NULL,
                course_id integer NOT NULL,
                'Review' text NOT NULL,
                FOREIGN KEY ('student_id') REFERENCES students (student_id),
                FOREIGN KEY ('course_id') REFERENCES courses (course_id)
                )"""
        )

        c.execute(
            "INSERT INTO reviews('student_id', 'course_id', Rating, Review) VALUES (?, ?, ?, ?)",
            (
                self.studentidBOX.text(),
                self.courseidBOX.text(),
                self.ratingBOX.text(),
                str(self.reviewBOX.text().upper()),
            ),
        )

        conn.commit()
        conn.close()

        # if course rating < 2 issue warning to instructor
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        inst_id = c.execute(
            """SELECT instructor_id FROM Courses WHERE course_id = (SELECT course_id FROM Enrollments WHERE student_id=?) """,
            (user.student_id,),
        ).fetchone()[0]

        # conn = sqlite3.connect("gsz.db")
        # c = conn.cursor()
        # c.execute(
        #     """SELECT instructor_id FROM courses
        #                     WHERE course_id =: course_id""",
        #     {"course_id": self.course_id},
        # )
        # instructor_id = c.fetchone[0]

        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """ SELECT avg(rating) From reviews WHERE course_id = (Select course_id FROM Courses WHERE instructor_id =:instructor_id)""",
            {"instructor_id": inst_id},
        )
        course_rating = c.fetchone()[0]
        conn.close()
        if course_rating < 2:
            issue_warning_instructor(inst_id)

        self.mainpage_home_student()

    def addApplicant(self, user_type):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sqlins = "INSERT INTO applicants(first, last, email, resume, user_type, approval_status) VALUES (?, ?, ?, ?, ?, ?)"
        sqlstd = "INSERT INTO applicants(first, last, email, gpa, num_courses_taken, user_type, approval_status) VALUES (?, ?, ?, ?, ?, ?, ?)"
        if user_type == "instructor":
            c.execute(
                sqlins,
                (
                    str(self.firstnameBOX.text()),
                    str(self.lastnameBOX.text()),
                    str(self.emailBOX.text()),
                    str(self.ResumeBOX.text()),
                    user_type,
                    "TBD",
                ),
            )
        else:
            c.execute(
                sqlstd,
                (
                    str(self.firstnameBOX.text()),
                    str(self.lastnameBOX.text()),
                    str(self.emailBOX.text()),
                    self.GPABOX.text(),
                    self.numcoursesBOX.text(),
                    user_type,
                    "TBD",
                ),
            )
        conn.commit()
        conn.close()
        self.startup_page()

    # Michael Start
    # instructor assign grades using student_id, course_id and grade
    # updates enrollments + students table
    def assign_grade(self):
        conn = sqlite3.connect("gsz.db")  # update enrollments
        c = conn.cursor()
        c.execute(
            """UPDATE enrollments SET grade=:grade
                        WHERE student_id=:student_id
                        AND course_id=:course_id""",
            {
                "grade": self.gradeBOX.text(),
                "student_id": self.studentIDBOX.text(),
                "course_id": self.courseIDBOX.text(),
            },
        )
        conn.commit()
        conn.close()
        # update students
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """UPDATE students SET semester_gpa=:grade
                        WHERE student_id=:student_id""",
            {"grade": self.gradeBOX.text(), "student_id": self.studentIDBOX.text()},
        )
        conn.commit()
        conn.close()
        self.mainpage_home_instructor()

    def assign_grade_page(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        self.mainW = QWidget()
        self.mainL = QHBoxLayout()

        self.boxesMegaW = QWidget()
        self.boxesMegaL = QHBoxLayout()

        self.boxesW = QWidget()
        self.boxesL = QVBoxLayout()
        self.boxesL.setAlignment(Qt.AlignCenter)

        self.boxesW2 = QWidget()
        self.boxesL2 = QVBoxLayout()
        self.boxesL2.setAlignment(Qt.AlignCenter)

        self.studentIDTXT = QtWidgets.QLabel()
        self.studentIDTXT.setText("Student ID :")
        self.studentIDTXT.setStyleSheet("color:white;")
        self.studentIDTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.studentIDTXT)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.studentIDBOX = QtWidgets.QLineEdit()
        self.studentIDBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.studentIDBOX.setFont(QFont("Century Gothic", 16))
        self.studentIDBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.studentIDBOX)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.courseIDTXT = QtWidgets.QLabel()
        self.courseIDTXT.setText("Course ID :")
        self.courseIDTXT.setStyleSheet("color:white;")
        self.courseIDTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.courseIDTXT)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.courseIDBOX = QtWidgets.QLineEdit()
        self.courseIDBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.courseIDBOX.setFont(QFont("Century Gothic", 16))
        self.courseIDBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.courseIDBOX)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.gradeTXT = QtWidgets.QLabel()
        self.gradeTXT.setText("Final Grade :")
        self.gradeTXT.setStyleSheet("color:white;")
        self.gradeTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.gradeTXT)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.gradeBOX = QtWidgets.QLineEdit()
        self.gradeBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.gradeBOX.setFont(QFont("Century Gothic", 16))
        self.gradeBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.gradeBOX)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        buttonsL = QHBoxLayout()
        buttonsW = QWidget()

        self.savegradeBTN = QtWidgets.QPushButton()
        self.savegradeBTN.setText("Save")
        self.savegradeBTN.setFont(QFont("Century Gothic", 20))
        self.savegradeBTN.setFixedSize(140, 40)
        self.savegradeBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.savegradeBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        buttonsL.addWidget(self.savegradeBTN)

        self.backBTN = QtWidgets.QPushButton()
        self.backBTN.setText("Back")
        self.backBTN.setFont(QFont("Century Gothic", 20))
        self.backBTN.setFixedSize(140, 40)
        self.backBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        buttonsL.addWidget(self.backBTN)

        buttonsW.setLayout(buttonsL)
        self.boxesL.addWidget(buttonsW)

        self.boxesW.setLayout(self.boxesL)
        self.boxesW2.setLayout(self.boxesL2)

        self.boxesMegaL.addWidget(self.boxesW)
        self.boxesMegaL.addWidget(self.boxesW2)
        self.boxesMegaW.setLayout(self.boxesMegaL)
        self.mainL.addWidget(self.boxesMegaW)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        self.savegradeBTN.clicked.connect(lambda: self.assign_grade())  # michael
        self.backBTN.clicked.connect(self.mainpage_home_instructor)
        # Michael End

    def instructorSignUp(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        self.mainW = QWidget()
        self.mainL = QHBoxLayout()

        self.boxesMegaW = QWidget()
        self.boxesMegaL = QHBoxLayout()

        self.boxesW = QWidget()
        self.boxesL = QVBoxLayout()
        self.boxesL.setAlignment(Qt.AlignCenter)

        self.boxesW2 = QWidget()
        self.boxesL2 = QVBoxLayout()
        self.boxesL2.setAlignment(Qt.AlignCenter)

        self.firstNameTXT = QtWidgets.QLabel()
        self.firstNameTXT.setText("First name :")
        self.firstNameTXT.setStyleSheet("color:white;")
        self.firstNameTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.firstNameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.firstnameBOX = QtWidgets.QLineEdit()
        self.firstnameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.firstnameBOX.setFont(QFont("Century Gothic", 16))
        self.firstnameBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.firstnameBOX)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.lastNameTXT = QtWidgets.QLabel()
        self.lastNameTXT.setText("Last name :")
        self.lastNameTXT.setStyleSheet("color:white;")
        self.lastNameTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.lastNameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.lastnameBOX = QtWidgets.QLineEdit()
        self.lastnameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.lastnameBOX.setFont(QFont("Century Gothic", 16))
        self.lastnameBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.lastnameBOX)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.emailTXT = QtWidgets.QLabel()
        self.emailTXT.setText("E-mail :")
        self.emailTXT.setStyleSheet("color:white;")
        self.emailTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.emailTXT)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.emailBOX = QtWidgets.QLineEdit()
        self.emailBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.emailBOX.setFont(QFont("Century Gothic", 16))
        self.emailBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.emailBOX)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.ResumeTXT = QtWidgets.QLabel()
        self.ResumeTXT.setText("Resume :")
        self.ResumeTXT.setStyleSheet("color:white;")
        self.ResumeTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.ResumeTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL2.addWidget(self.space)

        self.ResumeBOX = QtWidgets.QLineEdit()
        self.ResumeBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.ResumeBOX.setFont(QFont("Century Gothic", 16))
        self.ResumeBOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.ResumeBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL2.addWidget(self.space)

        buttonsL = QHBoxLayout()
        buttonsW = QWidget()

        self.saveBTN = QtWidgets.QPushButton()
        self.saveBTN.setText("Save")
        self.saveBTN.setFont(QFont("Century Gothic", 20))
        self.saveBTN.setFixedSize(140, 40)
        self.saveBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.saveBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        buttonsL.addWidget(self.saveBTN)

        self.backBTN = QtWidgets.QPushButton()
        self.backBTN.setText("Back")
        self.backBTN.setFont(QFont("Century Gothic", 20))
        self.backBTN.setFixedSize(140, 40)
        self.backBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        buttonsL.addWidget(self.backBTN)

        buttonsW.setLayout(buttonsL)
        self.boxesL.addWidget(buttonsW)

        self.boxesW.setLayout(self.boxesL)
        self.boxesW2.setLayout(self.boxesL2)

        self.boxesMegaL.addWidget(self.boxesW)
        self.boxesMegaL.addWidget(self.boxesW2)
        self.boxesMegaW.setLayout(self.boxesMegaL)
        self.mainL.addWidget(self.boxesMegaW)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        self.saveBTN.clicked.connect(lambda: self.addApplicant("instructor"))
        self.backBTN.clicked.connect(self.startup_page)

    def studentSignUp(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        self.mainW = QWidget()
        self.mainL = QHBoxLayout()

        self.boxesMegaW = QWidget()
        self.boxesMegaL = QHBoxLayout()

        self.boxesW = QWidget()
        self.boxesL = QVBoxLayout()
        self.boxesL.setAlignment(Qt.AlignCenter)

        self.boxesW2 = QWidget()
        self.boxesL2 = QVBoxLayout()
        self.boxesL2.setAlignment(Qt.AlignCenter)

        self.firstNameTXT = QtWidgets.QLabel()
        self.firstNameTXT.setText("First name :")
        self.firstNameTXT.setStyleSheet("color:white;")
        self.firstNameTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.firstNameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.firstnameBOX = QtWidgets.QLineEdit()
        self.firstnameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.firstnameBOX.setFont(QFont("Century Gothic", 16))
        self.firstnameBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.firstnameBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.secondNameTXT = QtWidgets.QLabel()
        self.secondNameTXT.setText("Middle name :")
        self.secondNameTXT.setStyleSheet("color:white;")
        self.secondNameTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.secondNameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.secondnameBOX = QtWidgets.QLineEdit()
        self.secondnameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.secondnameBOX.setFont(QFont("Century Gothic", 16))
        self.secondnameBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.secondnameBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.lastNameTXT = QtWidgets.QLabel()
        self.lastNameTXT.setText("Last name :")
        self.lastNameTXT.setStyleSheet("color:white;")
        self.lastNameTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.lastNameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.lastnameBOX = QtWidgets.QLineEdit()
        self.lastnameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.lastnameBOX.setFont(QFont("Century Gothic", 16))
        self.lastnameBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.lastnameBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.GPATXT = QtWidgets.QLabel()
        self.GPATXT.setText("GPA :")
        self.GPATXT.setStyleSheet("color:white;")
        self.GPATXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.GPATXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.GPABOX = QtWidgets.QLineEdit()
        self.GPABOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.GPABOX.setFont(QFont("Century Gothic", 16))
        self.GPABOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.GPABOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.emailTXT = QtWidgets.QLabel()
        self.emailTXT.setText("E-mail :")
        self.emailTXT.setStyleSheet("color:white;")
        self.emailTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.emailTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.emailBOX = QtWidgets.QLineEdit()
        self.emailBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.emailBOX.setFont(QFont("Century Gothic", 16))
        self.emailBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.emailBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.numcoursesTXT = QtWidgets.QLabel()
        self.numcoursesTXT.setText("# of courses taken :")
        self.numcoursesTXT.setStyleSheet("color:white;")
        self.numcoursesTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.numcoursesTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.numcoursesBOX = QtWidgets.QLineEdit()
        self.numcoursesBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.numcoursesBOX.setFont(QFont("Century Gothic", 16))
        self.numcoursesBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.numcoursesBOX)

        buttonsL = QHBoxLayout()
        buttonsW = QWidget()

        self.saveBTN = QtWidgets.QPushButton()
        self.saveBTN.setText("Save")
        self.saveBTN.setFont(QFont("Century Gothic", 20))
        self.saveBTN.setFixedSize(140, 40)
        self.saveBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.saveBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        buttonsL.addWidget(self.saveBTN)

        self.backBTN = QtWidgets.QPushButton()
        self.backBTN.setText("Back")
        self.backBTN.setFont(QFont("Century Gothic", 20))
        self.backBTN.setFixedSize(140, 40)
        self.backBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        buttonsL.addWidget(self.backBTN)

        buttonsW.setLayout(buttonsL)
        self.boxesL2.addWidget(buttonsW)

        self.boxesW.setLayout(self.boxesL)
        self.boxesW2.setLayout(self.boxesL2)

        self.boxesMegaL.addWidget(self.boxesW)
        self.boxesMegaL.addWidget(self.boxesW2)
        self.boxesMegaW.setLayout(self.boxesMegaL)
        self.mainL.addWidget(self.boxesMegaW)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        self.saveBTN.clicked.connect(lambda: self.addApplicant("student"))
        self.backBTN.clicked.connect(self.startup_page)

    def startup_page(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.classesTopStatesW = QWidget()
        self.classesTopStatesL = QHBoxLayout()

        self.space = QWidget()
        self.space.setFixedWidth(8)

        self.classesTopStatesL.addWidget(self.space)

        self.highestRatedClassesW = QWidget()
        self.highestRatedClassesL = QVBoxLayout()
        self.highestRatedClassesL.setAlignment(Qt.AlignHCenter)

        self.highestRatedClassesW.setFixedSize(380, 400)
        self.highestRatedClassesW.setStyleSheet(
            "border: 1px solid white;border-radius:15px;"
        )

        self.highestRatedClassesTXT = QtWidgets.QLabel()
        self.highestRatedClassesTXT.setText(display_highest_classes())
        self.highestRatedClassesTXT.setFont(QFont("Century Gothic", 20))
        self.highestRatedClassesTXT.setStyleSheet("border:0;color:white;")

        self.highestRatedClassesL.addWidget(self.highestRatedClassesTXT)

        self.highestRatedClassesW.setLayout(self.highestRatedClassesL)
        self.classesTopStatesL.addWidget(self.highestRatedClassesW)

        self.classesTopStatesL.addWidget(self.space)

        self.lowestRatedClassesW = QWidget()
        self.lowestRatedClassesL = QVBoxLayout()
        self.lowestRatedClassesL.setAlignment(Qt.AlignHCenter)

        self.lowestRatedClassesW.setFixedSize(380, 400)
        self.lowestRatedClassesW.setStyleSheet(
            "border: 1px solid white;border-radius:15px;"
        )

        self.lowestRatedClassesTXT = QtWidgets.QLabel()

        self.lowestRatedClassesTXT.setText(display_lowest_classes())

        self.lowestRatedClassesTXT.setFont(QFont("Century Gothic", 20))
        self.lowestRatedClassesTXT.setStyleSheet("border:0;color:white;")

        self.lowestRatedClassesL.addWidget(self.lowestRatedClassesTXT)

        self.lowestRatedClassesW.setLayout(self.lowestRatedClassesL)
        self.classesTopStatesL.addWidget(self.lowestRatedClassesW)

        self.classesTopStatesL.addWidget(self.space)

        self.highestGPAW = QWidget()
        self.highestGPAL = QVBoxLayout()
        self.highestGPAL.setAlignment(Qt.AlignHCenter)

        self.highestGPAW.setFixedSize(380, 400)
        self.highestGPAW.setStyleSheet("border: 1px solid white;border-radius:15px;")

        self.highestGPATXT = QtWidgets.QLabel()
        self.highestGPATXT.setText(display_honor_roll())
        self.highestGPATXT.setFont(QFont("Century Gothic", 20))
        self.highestGPATXT.setStyleSheet("border:0;color:white;")

        self.highestGPAL.addWidget(self.highestGPATXT)

        self.highestGPAW.setLayout(self.highestGPAL)
        self.classesTopStatesL.addWidget(self.highestGPAW)

        self.classesTopStatesL.addWidget(self.space)

        self.classesTopStatesW.setLayout(self.classesTopStatesL)
        self.mainL.addWidget(self.classesTopStatesW)

        self.space = QWidget()
        self.space.setFixedHeight(200)
        self.mainL.addWidget(self.space)

        self.logSignW = QWidget()
        self.logSignL = QHBoxLayout()
        self.logSignW.setFixedHeight(130)
        self.logSignL.setAlignment(Qt.AlignHCenter)

        self.logInBTN = QtWidgets.QPushButton()
        self.logInBTN.setText("Log In")
        self.logInBTN.setFont(QFont("Century Gothic", 20))
        self.logInBTN.setFixedSize(180, 60)
        self.logInBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.logInBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.logSignL.addWidget(self.logInBTN)

        self.signUpStudent = QtWidgets.QPushButton()
        self.signUpStudent.setText("Sign Up(Student)")
        self.signUpStudent.setFont(QFont("Century Gothic", 20))
        self.signUpStudent.setFixedSize(180, 60)
        self.signUpStudent.setCursor(QCursor(Qt.PointingHandCursor))
        self.signUpStudent.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.logSignL.addWidget(self.space)
        self.logSignL.addWidget(self.signUpStudent)

        # start of adding the back button

        self.signUpInstructor = QtWidgets.QPushButton()
        self.signUpInstructor.setText("Sign Up(Instructor)")
        self.signUpInstructor.setFont(QFont("Century Gothic", 20))
        self.signUpInstructor.setFixedSize(180, 60)
        self.signUpInstructor.setCursor(QCursor(Qt.PointingHandCursor))
        self.signUpInstructor.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.logSignL.addWidget(self.space)
        self.logSignL.addWidget(self.signUpInstructor)

        # ends of adding the back button

        self.logSignW.setLayout(self.logSignL)
        self.mainL.addWidget(self.logSignW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked
        self.logInBTN.clicked.connect(self.login_page)
        self.signUpInstructor.clicked.connect(self.instructorSignUp)
        self.signUpStudent.clicked.connect(self.studentSignUp)

    def student_complaint_page(self):
        self.setStyleSheet("background-color:#031926;")
        self.mainW = QWidget()
        self.mainL = QHBoxLayout()

        self.boxesMegaW = QWidget()
        self.boxesMegaL = QHBoxLayout()

        self.boxesW = QWidget()
        self.boxesL = QVBoxLayout()
        self.boxesL.setAlignment(Qt.AlignCenter)

        self.boxesW2 = QWidget()
        self.boxesL2 = QVBoxLayout()
        self.boxesL2.setAlignment(Qt.AlignCenter)

        self.firstNameTXT = QtWidgets.QLabel()
        self.firstNameTXT.setText("First name :")
        self.firstNameTXT.setStyleSheet("color:white;")
        self.firstNameTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.firstNameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.firstnameBOX = QtWidgets.QLineEdit()
        self.firstnameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.firstnameBOX.setFont(QFont("Century Gothic", 16))
        self.firstnameBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.firstnameBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.lastNameTXT = QtWidgets.QLabel()
        self.lastNameTXT.setText("Last name :")
        self.lastNameTXT.setStyleSheet("color:white;")
        self.lastNameTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.lastNameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.lastnameBOX = QtWidgets.QLineEdit()
        self.lastnameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.lastnameBOX.setFont(QFont("Century Gothic", 16))
        self.lastnameBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.lastnameBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.reasonofcomplaintTXT = QtWidgets.QLabel()
        self.reasonofcomplaintTXT.setText("Reason of complaint :")
        self.reasonofcomplaintTXT.setStyleSheet("color:white;")
        self.reasonofcomplaintTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.reasonofcomplaintTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.reasonofcomplaintBOX = QtWidgets.QLineEdit()
        self.reasonofcomplaintBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.reasonofcomplaintBOX.setFont(QFont("Century Gothic", 16))
        self.reasonofcomplaintBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.reasonofcomplaintBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.complaintTXT = QtWidgets.QLabel()
        self.complaintTXT.setText("Complaint :")
        self.complaintTXT.setStyleSheet("color:white;")
        self.complaintTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.complaintTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.complaintBOX = QtWidgets.QLineEdit()
        self.complaintBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.complaintBOX.setFont(QFont("Century Gothic", 16))
        self.complaintBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.complaintBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.submitFBTN = QtWidgets.QPushButton()
        self.submitFBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.submitFBTN.setText("Submit Complaint")
        self.submitFBTN.setFont(QFont("Century Gothic", 20))
        self.submitFBTN.setFixedSize(180, 60)
        self.submitFBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.boxesL.addWidget(self.submitFBTN)

        self.back = QtWidgets.QPushButton()
        self.back.setText("Back")
        self.back.setFont(QFont("Century Gothic", 20))
        self.back.setFixedSize(180, 60)
        self.back.setCursor(QCursor(Qt.PointingHandCursor))
        self.back.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.boxesL.addWidget(self.back)

        self.boxesW.setLayout(self.boxesL)
        self.mainL.addWidget(self.boxesW)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        self.back.clicked.connect(self.mainpage_home_student)
        self.submitFBTN.clicked.connect(self.complain)

    # Joel
    def complain(self):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        # complainee
        result = c.execute(
            "SELECT user_id FROM users WHERE first=:first and last=:last ",
            {"first": self.firstnameBOX.text(), "last": self.lastnameBOX.text()},
        ).fetchone()[0]

        complaint_type = " "
        description = self.reasonofcomplaintBOX.text() + " " + self.complaintBOX.text()

        sql = "INSERT INTO complaints(complainant_id, complainee_id, description, complaint_type) VALUES(?, ?, ?, ?)"
        c.execute(sql, (user.user_id, result, description, complaint_type))
        conn.commit()
        conn.close()

        self.mainpage_home_student()

    # instructor_complaint
    def instructor_complaint_page(self):
        self.setStyleSheet("background-color:#031926;")
        self.mainW = QWidget()
        self.mainL = QHBoxLayout()

        self.boxesMegaW = QWidget()
        self.boxesMegaL = QHBoxLayout()

        self.boxesW = QWidget()
        self.boxesL = QVBoxLayout()
        self.boxesL.setAlignment(Qt.AlignCenter)

        self.boxesW2 = QWidget()
        self.boxesL2 = QVBoxLayout()
        self.boxesL2.setAlignment(Qt.AlignCenter)

        self.firstNameTXT = QtWidgets.QLabel()
        self.firstNameTXT.setText("First name :")
        self.firstNameTXT.setStyleSheet("color:white;")
        self.firstNameTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.firstNameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.firstnameBOX = QtWidgets.QLineEdit()
        self.firstnameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.firstnameBOX.setFont(QFont("Century Gothic", 16))
        self.firstnameBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.firstnameBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.lastNameTXT = QtWidgets.QLabel()
        self.lastNameTXT.setText("Last name :")
        self.lastNameTXT.setStyleSheet("color:white;")
        self.lastNameTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.lastNameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.lastnameBOX = QtWidgets.QLineEdit()
        self.lastnameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.lastnameBOX.setFont(QFont("Century Gothic", 16))
        self.lastnameBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.lastnameBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.reasonofcomplaintTXT = QtWidgets.QLabel()
        self.reasonofcomplaintTXT.setText("Reason of complaint :")
        self.reasonofcomplaintTXT.setStyleSheet("color:white;")
        self.reasonofcomplaintTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.reasonofcomplaintTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.reasonofcomplaintBOX = QtWidgets.QLineEdit()
        self.reasonofcomplaintBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.reasonofcomplaintBOX.setFont(QFont("Century Gothic", 16))
        self.reasonofcomplaintBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.reasonofcomplaintBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.complaintTXT = QtWidgets.QLabel()
        self.complaintTXT.setText("Complaint :")
        self.complaintTXT.setStyleSheet("color:white;")
        self.complaintTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.complaintTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.complaintBOX = QtWidgets.QLineEdit()
        self.complaintBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.complaintBOX.setFont(QFont("Century Gothic", 16))
        self.complaintBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.complaintBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.complaintypeTXT = QtWidgets.QLabel()
        self.complaintypeTXT.setText("Complaint Type :")
        self.complaintypeTXT.setStyleSheet("color:white;")
        self.complaintypeTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.complaintypeTXT)

        self.complaintypeBOX = QtWidgets.QLineEdit()
        self.complaintypeBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.complaintypeBOX.setFont(QFont("Century Gothic", 16))
        self.complaintypeBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.complaintypeBOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL.addWidget(self.space)

        self.submitFBTN = QtWidgets.QPushButton()
        self.submitFBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.submitFBTN.setText("Submit Complaint")
        self.submitFBTN.setFont(QFont("Century Gothic", 20))
        self.submitFBTN.setFixedSize(180, 60)
        self.submitFBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.boxesL.addWidget(self.submitFBTN)

        self.back = QtWidgets.QPushButton()
        self.back.setText("Back")
        self.back.setFont(QFont("Century Gothic", 20))
        self.back.setFixedSize(180, 60)
        self.back.setCursor(QCursor(Qt.PointingHandCursor))
        self.back.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.boxesL.addWidget(self.back)

        self.boxesW.setLayout(self.boxesL)
        self.mainL.addWidget(self.boxesW)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        self.back.clicked.connect(self.mainpage_home_instructor)
        self.submitFBTN.clicked.connect(self.complain)
        # instructor complaint

        # Start

    def issuewarning_page_registrar(self):  # Merge Start
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QHBoxLayout()

        # ----------------Design-----------------

        self.boxesW = QWidget()
        self.boxesL = QVBoxLayout()

        self.useridTXT = QtWidgets.QLabel()
        self.useridTXT.setText("User Id :")
        self.useridTXT.setStyleSheet("color:white;")
        self.useridTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.useridTXT)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL.addWidget(self.space)

        self.useridBOX = QtWidgets.QLineEdit()
        self.useridBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.useridBOX.setFont(QFont("Century Gothic", 20))
        self.useridBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.useridBOX)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL.addWidget(self.space)

        self.btnsW = QWidget()
        self.btnsL = QHBoxLayout()

        self.space = QWidget()
        self.space.setFixedWidth(30)
        self.btnsL.addWidget(self.space)

        # Start
        self.sssssBTN = QtWidgets.QPushButton()
        self.sssssBTN.setText("Warn")
        self.sssssBTN.setFont(QFont("Century Gothic", 20))
        self.sssssBTN.setFixedSize(180, 60)
        self.sssssBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.sssssBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.sssssBTN)
        self.BTNSW.setLayout(self.BTNSL)

        # End
        self.space = QWidget()
        self.space.setFixedHeight(200)
        self.boxesL.addWidget(self.space)

        # Start mike
        self.expelBTN = QtWidgets.QPushButton()
        self.expelBTN.setText("Expel")
        self.expelBTN.setFont(QFont("Century Gothic", 20))
        self.expelBTN.setFixedSize(180, 60)
        self.expelBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.expelBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.expelBTN)
        self.BTNSW.setLayout(self.BTNSL)

        self.graduateBTN = QtWidgets.QPushButton()
        self.graduateBTN.setText("Graduate")
        self.graduateBTN.setFont(QFont("Century Gothic", 20))
        self.graduateBTN.setFixedSize(180, 60)
        self.graduateBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.graduateBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.expelBTN)
        self.BTNSW.setLayout(self.BTNSL)

        # mike End

        self.backToMainBTN = QtWidgets.QPushButton()
        self.backToMainBTN.setText("Back")
        self.backToMainBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToMainBTN.setFont(QFont("Century Gothic", 20))
        self.backToMainBTN.setFixedSize(180, 60)
        self.backToMainBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.btnsL.addWidget(self.backToMainBTN)
        self.mainL.addWidget(self.sssssBTN)  # Aiman
        self.mainL.addWidget(self.expelBTN)
        self.mainL.addWidget(self.graduateBTN)

        self.btnsW.setLayout(self.btnsL)
        self.boxesL.addWidget(self.btnsW)

        self.boxesW.setLayout(self.boxesL)
        self.mainL.addWidget(self.boxesW)
        self.mainW.setLayout(self.mainL)

        self.space = QWidget()
        self.space.setFixedWidth(180)

        self.mainL.addWidget(self.space)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked
        self.backToMainBTN.clicked.connect(self.mainpage_home_registrar)
        self.sssssBTN.clicked.connect(self.issue_warning_user)
        self.expelBTN.clicked.connect(self.expel_user)
        self.graduateBTN.clicked.connect(self.graduate_student)
        # self.signUpBTN.clicked.connect(self.signup_page)
        # self.loginFBTN.clicked.connect(self.login)

    def graduate_student(self):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        user_type = c.execute(
            "SELECT user_type From users where user_id = :user_id",
            {"user_id": self.useridBOX.text()},
        ).fetchone()[0]
        if user_type == "student":
            c.execute(
                """UPDATE students SET Degree = 'Masters'
                                WHERE student_id = (SELECT student_id FROM students WHERE user_id =:user_id)""",
                {"user_id": self.useridBOX.text()},
            )
            conn.commit()
            conn.close()
            self.mainpage_home_registrar()
            return
        print("cannot graduate non students")
        self.mainpage_home_registrar()

    def expel_user(self):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        # get user type
        user_type = c.execute(
            "SELECT user_type From users where user_id = :user_id",
            {"user_id": self.useridBOX.text()},
        ).fetchone()[0]
        if user_type == "Registrar":
            print("cannot expel registrars")
            self.mainpage_home_registrar()

        c.execute(
            "DELETE FROM users WHERE user_id=:user_id",
            {"user_id": self.useridBOX.text()},
        )
        conn.commit()
        conn.close()
        self.mainpage_home_registrar()

    def issue_warning_user(self):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        # get user type
        user_type = c.execute(
            "SELECT user_type From users where user_id = :user_id",
            {"user_id": self.useridBOX.text()},
        ).fetchone()[0]
        if user_type == "Registrar":
            print("cannot warn registrars")
            self.mainpage_home_registrar()
        if user_type == "instructor":
            c.execute(
                "SELECT warning_count From instructors where user_id = :user_id",
                {"user_id": self.useridBOX.text()},
            )
            new_warning_count = (
                c.fetchone()[0] + 1
            )  # c.fetchone()[0] isolate variable from tuple
            # print(new_warning_count)
            # update student warning_count
            c.execute(
                """UPDATE instructors SET warning_count = :new_warning_count
                                    WHERE user_id =:user_id""",
                {
                    "user_id": self.useridBOX.text(),
                    "new_warning_count": new_warning_count,
                },
            )
            conn.commit()
            conn.close()
            self.mainpage_home_registrar()
        if user_type == "student":
            c.execute(
                "SELECT warning_count From students where user_id = :user_id",
                {"user_id": self.useridBOX.text()},
            )
            new_warning_count = (
                c.fetchone()[0] + 1
            )  # c.fetchone()[0] isolate variable from tuple
            # print(new_warning_count)
            # update student warning_count
            c.execute(
                """UPDATE students SET warning_count = :new_warning_count
                                    WHERE user_id =:user_id""",
                {
                    "user_id": self.useridBOX.text(),
                    "new_warning_count": new_warning_count,
                },
            )
            conn.commit()
            conn.close()
            self.mainpage_home_registrar()

        # Merge End

        # Merge Start?

    def inst_complain(self):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        # complainee
        result = c.execute(
            "SELECT user_id FROM users WHERE first=:first and last=:last ",
            {"first": self.firstnameBOX.text(), "last": self.lastnameBOX.text()},
        ).fetchone()[0]

        complaint_type = self.complaintypeBOX.text()
        description = self.complaintBOX.text()

        sql = "INSERT INTO complaints(complainant_id, complainee_id, description, complaint_type) VALUES(?, ?, ?, ?)"
        c.execute(sql, (user.user_id, result, description, complaint_type))
        conn.commit()
        conn.close()

        self.mainpage_home_student()

    def complaint_page_registrar(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.main_contentW = QWidget()
        self.main_contentL = QVBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        complaint = sqlite3.connect("gsz.db")
        df = display_db.pd.read_sql_query("SELECT * FROM complaints", complaint)

        self.model = display_db.pandasModel(df)
        self.view = QTableView()
        self.view.setModel(self.model)
        ids = []
        cboxes = []
        index = 0

        self.view.resize(800, 600)
        self.view.show()

        self.main_contentW.setLayout(self.main_contentL)

        self.back = QtWidgets.QPushButton()
        self.back.setText("Back")
        self.back.setFont(QFont("Century Gothic", 20))
        self.back.setFixedSize(180, 60)
        self.back.setCursor(QCursor(Qt.PointingHandCursor))
        self.back.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.mainL.addWidget(self.back)
        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        # self.sssssBTN = QtWidgets.QPushButton()
        # self.sssssBTN.setText("Submit")
        # self.sssssBTN.setFont(QFont("Century Gothic", 20))
        # self.sssssBTN.setFixedSize(180, 60)
        # self.sssssBTN.setCursor(QCursor(Qt.PointingHandCursor))
        # self.sssssBTN.setStyleSheet(
        #     "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
        #     "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        # )
        # self.BTNSL.addWidget(self.sssssBTN)
        # self.BTNSW.setLayout(self.BTNSL)

        # -------------End of Design-------------

        # applicant = sqlite3.connect("gsz.db")
        # df = display_db.pd.read_sql_query("SELECT * FROM applicants", applicant)
        # df = df.drop(["num_courses_taken", "applicant_id"], axis=1)

        # model = display_db.pandasModel(df)
        # view = QTableView()
        # view.setModel(model)
        # view.resize(800, 600)
        # view.show()

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked
        # self.mainL.addWidget(self.sssssBTN)

        self.back.clicked.connect(self.mainpage_home_registrar)

    def signup_page(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QHBoxLayout()

        # ----------------Design-----------------

        self.boxesW = QWidget()
        self.boxesL = QVBoxLayout()

        self.idTXT = QtWidgets.QLabel()
        self.idTXT.setText("Name :")
        self.idTXT.setStyleSheet("color:white;")
        self.idTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.idTXT)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.idBOX = QtWidgets.QLineEdit()
        self.idBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.idBOX.setFont(QFont("Century Gothic", 20))
        self.idBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.idBOX)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.emailTXT = QtWidgets.QLabel()
        self.emailTXT.setText("E-mail :")
        self.emailTXT.setStyleSheet("color:white;")
        self.emailTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.emailTXT)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.emailBOX = QtWidgets.QLineEdit()
        self.emailBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.emailBOX.setFont(QFont("Century Gothic", 20))
        self.emailBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.emailBOX)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.passwordTXT = QtWidgets.QLabel()
        self.passwordTXT.setText("Password :")
        self.passwordTXT.setStyleSheet("color:white;")
        self.passwordTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.passwordTXT)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.passwordBOX = QtWidgets.QLineEdit()
        self.passwordBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.passwordBOX.setFont(QFont("Century Gothic", 20))
        self.passwordBOX.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.passwordBOX)

        self.boxesW.setLayout(self.boxesL)
        self.mainL.addWidget(self.boxesW)
        self.mainW.setLayout(self.mainL)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.buttonsW = QWidget()
        self.buttonsL = QHBoxLayout()

        self.signUpFBTN = QtWidgets.QPushButton()
        self.signUpFBTN.setText("Sign Up")
        self.signUpFBTN.setFont(QFont("Century Gothic", 20))
        self.signUpFBTN.setFixedSize(180, 60)
        self.signUpFBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.signUpFBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.buttonsL.addWidget(self.signUpFBTN)

        self.space = QWidget()
        self.space.setFixedWidth(30)
        self.buttonsL.addWidget(self.space)

        self.backToMainBTN = QtWidgets.QPushButton()
        self.backToMainBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToMainBTN.setText("Back")
        self.backToMainBTN.setFont(QFont("Century Gothic", 20))
        self.backToMainBTN.setFixedSize(180, 60)
        self.backToMainBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.buttonsL.addWidget(self.backToMainBTN)

        self.buttonsW.setLayout(self.buttonsL)

        self.combo = QtWidgets.QComboBox()
        self.combo.setStyleSheet(
            "QComboBox{color:white;background-color:#076DF2;border-radius:10;"
            "margin-left:110px;padding-left:10px;}"
            "QComboBox::drop-down { "
            "subcontrol-origin: padding;"
            "subcontrol-position: top right; "
            "width: 15px; "
            "border-left-width: 1px; "
            "border-left-color: #076DF2; "
            "border-left-style: solid; "
            "border-top-right-radius: 10px; "
            "border-bottom-right-radius: 10px; "
            "}"
            "QComboBox:on{border-bottom-right-radius:0;border-bottom-left-radius:0;}"
            "QComboBox QAbstractItemView {"
            "background:#076DF2;"
            "selection-background-color: #03469e;}"
        )
        for i in ["Student", "Instructor"]:
            self.combo.addItem(i)

        self.combo.setFont(QFont("Myriad Pro", 18))
        self.combo.setFixedSize(500, 50)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL.addWidget(self.combo)
        self.boxesL.addWidget(self.space)
        self.boxesL.addWidget(self.buttonsW)

        self.boxesW.setLayout(self.buttonsL)
        self.mainL.addWidget(self.boxesW)
        self.mainW.setLayout(self.mainL)

        self.space = QWidget()
        self.space.setFixedWidth(180)

        self.mainL.addWidget(self.space)

        self.tipsW = QWidget()
        self.tipsL = QVBoxLayout()

        self.tipsW.setFixedSize(400, 600)
        self.tipsW.setStyleSheet("border: 1px solid white;border-radius: 10px;")

        self.tipsTXT = QtWidgets.QTextEdit()
        self.tipsTXT.setText(
            "\nOnly the registrar can decide to accept or reject the application."
            " Any student whose GPA is less than 3.0 and the program quota isn't reached"
            " will be accepted and rejected otherwise, you sill receive a unique"
            " ID after your first login."
        )

        self.tipsTXT.setFont(QFont("Century Gothic", 20))
        self.tipsTXT.setAlignment(Qt.AlignHCenter)
        self.tipsTXT.setStyleSheet("color:white;border:0;")

        self.tipsL.addWidget(self.tipsTXT)

        self.tipsW.setLayout(self.tipsL)
        self.mainL.addWidget(self.tipsW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked
        self.backToMainBTN.clicked.connect(self.StartupStudent)
        self.signUpFBTN.clicked.connect(self.signup)
        self.signUpBTN.clicked.connect(self.signup_page)

    def login_page(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QHBoxLayout()

        # ----------------Design-----------------

        self.boxesW = QWidget()
        self.boxesL = QVBoxLayout()

        self.logo = QtWidgets.QLabel()
        self.logo.setPixmap(QPixmap("logo.png"))
        self.boxesL.addWidget(self.logo)

        self.nameTXT = QtWidgets.QLabel()
        self.nameTXT.setText("Id :")
        self.nameTXT.setStyleSheet("color:white;")
        self.nameTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.nameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL.addWidget(self.space)

        self.idBOX = QtWidgets.QLineEdit()
        self.idBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.idBOX.setFont(QFont("Century Gothic", 20))
        self.idBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.idBOX)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL.addWidget(self.space)

        self.passwordTXT = QtWidgets.QLabel()
        self.passwordTXT.setText("Password :")
        self.passwordTXT.setStyleSheet("color:white;")
        self.passwordTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.passwordTXT)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL.addWidget(self.space)

        self.passwordBOX = QtWidgets.QLineEdit()
        self.passwordBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.passwordBOX.setFont(QFont("Century Gothic", 20))
        self.passwordBOX.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.passwordBOX)

        self.boxesW.setLayout(self.boxesL)
        self.mainL.addWidget(self.boxesW)
        self.mainW.setLayout(self.mainL)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL.addWidget(self.space)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL.addWidget(self.space)

        self.btnsW = QWidget()
        self.btnsL = QHBoxLayout()

        self.loginFBTN = QtWidgets.QPushButton()
        self.loginFBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.loginFBTN.setText("Log in")
        self.loginFBTN.setFont(QFont("Century Gothic", 20))
        self.loginFBTN.setFixedSize(180, 60)
        self.loginFBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.btnsL.addWidget(self.loginFBTN)

        self.space = QWidget()
        self.space.setFixedWidth(30)
        self.btnsL.addWidget(self.space)

        self.backToMainBTN = QtWidgets.QPushButton()
        self.backToMainBTN.setText("Back")
        self.backToMainBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToMainBTN.setFont(QFont("Century Gothic", 20))
        self.backToMainBTN.setFixedSize(180, 60)
        self.backToMainBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.btnsL.addWidget(self.backToMainBTN)
        self.btnsW.setLayout(self.btnsL)
        self.boxesL.addWidget(self.btnsW)

        self.boxesW.setLayout(self.boxesL)
        self.mainL.addWidget(self.boxesW)
        self.mainW.setLayout(self.mainL)

        self.space = QWidget()
        self.space.setFixedWidth(180)

        self.mainL.addWidget(self.space)

        self.tipsW = QWidget()
        self.tipsL = QVBoxLayout()

        self.tipsW.setFixedSize(400, 600)
        self.tipsW.setStyleSheet("border: 1px solid white;border-radius: 10px;")

        self.tipsTXT = QtWidgets.QTextEdit()
        self.tipsTXT.setText(
            "\nOnly the registrar can decide to accept or reject the application."
            " Any student whose GPA is less than 3.0 and the program quota isn't reached"
            " will be accepted and rejected otherwise, you sill receive a unique"
            " ID after your first login."
        )

        self.tipsTXT.setFont(QFont("Century Gothic", 20))
        self.tipsTXT.setAlignment(Qt.AlignHCenter)
        self.tipsTXT.setStyleSheet("color:white;border:0;")

        self.tipsL.addWidget(self.tipsTXT)

        self.tipsW.setLayout(self.tipsL)
        self.mainL.addWidget(self.tipsW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked
        self.backToMainBTN.clicked.connect(self.startup_page)
        # self.signUpBTN.clicked.connect(self.signup_page)
        self.loginFBTN.clicked.connect(self.login)

    def mainpage_home_student(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        self.BTNSW = QWidget()
        self.BTNSL = QHBoxLayout()

        self.ComplaintBTN = QtWidgets.QPushButton()
        self.ComplaintBTN.setFont(QFont("Century Gothic", 20))
        self.ComplaintBTN.setFixedSize(180, 60)
        self.ComplaintBTN.setText("Complaint")
        self.ComplaintBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.ComplaintBTN)

        self.reviewBTN = QtWidgets.QPushButton()  # Michael test
        self.reviewBTN.setFont(QFont("Century Gothic", 20))
        self.reviewBTN.setFixedSize(180, 60)
        self.reviewBTN.setText("Review")
        self.reviewBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.reviewBTN)

        self.WarningsBTN = QtWidgets.QPushButton()  # Aiman test
        self.WarningsBTN.setFont(QFont("Century Gothic", 20))
        self.WarningsBTN.setFixedSize(180, 60)
        self.WarningsBTN.setText("Warnings")
        self.WarningsBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.WarningsBTN)

        self.graduationBTN = QtWidgets.QPushButton()  # Aiman test
        self.graduationBTN.setFont(QFont("Century Gothic", 20))
        self.graduationBTN.setFixedSize(180, 60)
        self.graduationBTN.setText("Graduation")
        self.graduationBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.graduationBTN)  # Aiman

        self.logoutBTN = QtWidgets.QPushButton()
        self.logoutBTN.setText("Logout")
        self.logoutBTN.setFont(QFont("Century Gothic", 20))
        self.logoutBTN.setFixedSize(180, 60)
        self.logoutBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.logoutBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.logoutBTN)

        self.BTNSW.setLayout(self.BTNSL)

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setFixedHeight(200)
        self.logo.setFixedWidth(200)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.space = QWidget()
        self.space.setFixedHeight(385)

        self.logoL.addWidget(self.logo)
        self.logoL.addWidget(self.space)
        self.logoL.addWidget(self.BTNSW)

        self.logoW.setLayout(self.logoL)
        self.main_contentL.addWidget(self.logoW)
        self.main_contentW.setLayout(self.main_contentL)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked
        self.home.clicked.connect(self.mainpage_home_student)
        self.account.clicked.connect(self.mainpage_account)
        self.logoutBTN.clicked.connect(self.startup_page)
        self.help.clicked.connect(self.mainpage_help)
        self.ComplaintBTN.clicked.connect(self.student_complaint_page)
        self.classes.clicked.connect(self.mainpage_classes)
        self.reviewBTN.clicked.connect(self.add_review_page)  # Michael Test
        self.WarningsBTN.clicked.connect(self.Warning_page_students)  # Aiman

    # AIman
    def Warning_page_students(self):
        self.setStyleSheet("background-color:#031926;")
        self.mainW = QWidget()
        self.mainL = QHBoxLayout()
        self.mainL.setAlignment(Qt.AlignRight)

        self.back = QtWidgets.QPushButton()  # Aiman
        self.back.setText("Warnings")
        self.back.setFont(QFont("Century Gothic", 50))
        self.back.setFixedSize(500, 70)
        self.back.setCursor(QCursor(Qt.PointingHandCursor))
        self.back.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.mainL.addWidget(self.back)  # Aiman

        self.back = QtWidgets.QPushButton()
        self.back.setText("Back")
        self.back.setFont(QFont("Century Gothic", 20))
        self.back.setFixedSize(180, 60)
        self.back.setCursor(QCursor(Qt.PointingHandCursor))
        self.back.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.mainL.addWidget(self.back)
        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        self.back.clicked.connect(self.mainpage_home_student)

        # End

    def mainpage_account(self):
        global id
        global acc_type
        global name
        global email
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        self.logOut = QtWidgets.QPushButton()
        self.logOut.setFont(QFont("Century Gothic", 20))
        self.logOut.setFixedSize(180, 60)
        self.logOut.setText("Log out")
        self.logOut.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setFixedHeight(200)
        self.logo.setFixedWidth(200)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.space = QWidget()

        self.logoL.addWidget(self.logo)
        self.logoL.addWidget(self.space)
        self.logoL.addWidget(self.logOut)

        self.logoW.setLayout(self.logoL)
        self.main_contentL.addWidget(self.logoW)

        self.accountDataW = QWidget()
        self.accountDataL = QVBoxLayout()
        self.accountDataL.setAlignment(Qt.AlignHCenter)

        self.accountDataW.setFixedSize(480, 660)
        self.accountDataW.setStyleSheet(
            "border: 1px solid white;border-radius:15px;margin-top:30px;"
        )

        self.accountNameTXT = QtWidgets.QLabel()
        self.accountNameTXT.setText("Account name :")
        self.accountNameTXT.setStyleSheet("color:white; border:0;")
        self.accountNameTXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountNameTXT)

        self.accountName = QtWidgets.QLabel()
        self.accountName.setText(name)
        self.accountName.setStyleSheet("color:#0583F2; border:0;")
        self.accountName.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountName)

        self.email_TXT = QtWidgets.QLabel()
        self.email_TXT.setText("E-mail :")
        self.email_TXT.setStyleSheet("color:white; border:0;")
        self.email_TXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.email_TXT)

        self.email = QtWidgets.QLabel()
        self.email.setText(email)
        self.email.setStyleSheet("color:#0583F2; border:0;")
        self.email.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.email)

        self.idTXT = QtWidgets.QLabel()
        self.idTXT.setText("Student ID :")
        self.idTXT.setStyleSheet("color:white; border:0;")
        self.idTXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.idTXT)

        self.accountId = QtWidgets.QLabel()
        self.accountId.setText(id)
        self.accountId.setStyleSheet("color:#0583F2; border:0;")
        self.accountId.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountId)

        self.accountTypeTXT = QtWidgets.QLabel()
        self.accountTypeTXT.setText("Account type :")
        self.accountTypeTXT.setStyleSheet("color:white; border:0;")
        self.accountTypeTXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountTypeTXT)

        self.accountType = QtWidgets.QLabel()  # Aiman WHY?
        self.accountType.setText("Student")
        self.accountType.setStyleSheet("color:#0583F2; border:0;")
        self.accountType.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountType)

        self.accountDataW.setLayout(self.accountDataL)
        self.main_contentL.addWidget(self.accountDataW)
        self.main_contentW.setLayout(self.main_contentL)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.home.clicked.connect(self.mainpage_home_student)
        self.account.clicked.connect(self.mainpage_account)
        self.help.clicked.connect(self.mainpage_help)
        self.logOut.clicked.connect(self.logout)
        self.classes.clicked.connect(self.mainpage_classes)

    def mainpage_help(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        # self.BTNSW = QWidget()
        # self.BTNSL = QHBoxLayout()

        # self.backToStartupBTN = QtWidgets.QPushButton()
        # self.backToStartupBTN.setText("Back")
        # self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        # self.backToStartupBTN.setFixedSize(180, 60)
        # self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        # self.backToStartupBTN.setStyleSheet(
        #     "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
        #     "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        # )
        # self.BTNSL.addWidget(self.backToStartupBTN)

        # self.BTNSW.setLayout(self.BTNSL)

        # self.logo = QtWidgets.QLabel(self.logoW)
        # self.logo.setFixedHeight(200)
        # self.logo.setFixedWidth(200)
        # self.logo.setPixmap(QPixmap("logo.png"))
        # self.space = QWidget()
        # self.space.setFixedHeight(385)

        # self.logoL.addWidget(self.logo)
        # self.logoL.addWidget(self.space)
        # self.logoL.addWidget(self.BTNSW)

        # self.logoW.setLayout(self.logoL)
        # self.main_contentL.addWidget(self.logoW)
        self.main_contentW.setLayout(self.main_contentL)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)
        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.home.clicked.connect(self.mainpage_home_student)
        self.account.clicked.connect(self.mainpage_account)
        self.help.clicked.connect(self.mainpage_help)
        self.classes.clicked.connect(self.mainpage_classes)
        # self.backToStartupBTN.clicked.connect(self.StartupStudent)

    def mainpage_classes(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QVBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        self.BTNSW = QWidget()
        self.BTNSL = QHBoxLayout()

        # self.backToStartupBTN = QtWidgets.QPushButton()
        # self.backToStartupBTN.setText("Back")
        # self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        # self.backToStartupBTN.setFixedSize(180, 60)
        # self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        # self.backToStartupBTN.setStyleSheet(
        # "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
        # "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        # )
        # self.BTNSL.addWidget(self.backToStartupBTN)

        self.BTNSW.setLayout(self.BTNSL)

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setFixedHeight(200)
        self.logo.setFixedWidth(200)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.space = QWidget()
        self.space.setFixedHeight(85)

        self.logoL.addWidget(self.logo)
        self.logoL.addWidget(self.space)

        self.logoW.setLayout(self.logoL)
        # self.main_contentL.addWidget(self.logoW)
        self.main_contentW.setLayout(self.main_contentL)

        # ------------------------start-----------------------------

        # global classes
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "SELECT course_name, course_time, instructor_id, course_size, enroll_count FROM courses"
        c.execute(sql)
        classes = c.fetchall()
        print(classes)

        if classes != None:
            for i in classes:
                sql = "SELECT user_id FROM instructors WHERE instructor_id = ?"
                i = list(i)
                c.execute(sql, (i[2],))
                user_id = c.fetchone()[0]
                ins = Instructor(user_id)
                i[2] = ins.first + " " + ins.last
                self.classesW = QWidget()
                self.classesL = QVBoxLayout()
                self.StudentClassW = QtWidgets.QWidget()
                self.StudentClassW.setStyleSheet(
                    "background-color:white;border-radius:15px;"
                )
                self.StudentClassL = QHBoxLayout()

                self.className = QtWidgets.QLabel()
                self.className.setFixedWidth(180)
                self.className.setText(i[0])
                self.className.setFont(QFont("Century Gothic", 14))

                self.classTime = QtWidgets.QLabel()
                self.classTime.setText(f"Time:\n\n{i[1]}")
                self.classTime.setFont(QFont("Century Gothic", 14))

                self.instructorName = QtWidgets.QLabel()
                self.instructorName.setText(f"Instructor:\n\n{i[2]}")
                self.instructorName.setFont(QFont("Century Gothic", 14))

                self.seats = QtWidgets.QLabel()
                self.seats.setText(f"Seats:\n\n{i[3]}")
                self.seats.setFont(QFont("Century Gothic", 14))

                self.addBTN = QtWidgets.QPushButton()
                self.addBTN.setText("Add")
                self.addBTN.setFont(QFont("Century Gothic", 14))
                self.addBTN.setFixedSize(100, 60)
                self.addBTN.setStyleSheet(
                    "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
                    "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
                )

                self.StudentClassL.addWidget(self.className)
                self.StudentClassL.addWidget(self.classTime)
                self.StudentClassL.addWidget(self.instructorName)
                self.StudentClassL.addWidget(self.seats)
                self.StudentClassL.addWidget(self.addBTN)

                self.StudentClassW.setLayout(self.StudentClassL)
                self.classesL.addWidget(self.StudentClassW)

                self.addBTN.clicked.connect(
                    partial(self.addClass, self.addBTN)
                )  # Aiman 11/6
                self.classesW.setLayout(self.classesL)
                self.main_contentL.addWidget(self.classesW)
                self.main_contentL.addWidget(self.BTNSW)

        # -------------------------end------------------------------

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.home.clicked.connect(self.mainpage_home_student)
        self.account.clicked.connect(self.mainpage_account)
        self.help.clicked.connect(self.mainpage_help)
        self.classes.clicked.connect(self.mainpage_classes)
        # self.backToStartupBTN.clicked.connect(self.mainpage_home_student)

    def mainpage_home_instructor(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        self.BTNSW = QWidget()
        self.BTNSL = QHBoxLayout()

        self.ComplaintBTN = QtWidgets.QPushButton()
        self.ComplaintBTN.setFont(QFont("Century Gothic", 20))
        self.ComplaintBTN.setFixedSize(180, 60)
        self.ComplaintBTN.setText("Complaint")
        self.ComplaintBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.ComplaintBTN)

        self.assignGradeBTN = QtWidgets.QPushButton()  # Michael test
        self.assignGradeBTN.setFont(QFont("Century Gothic", 20))
        self.assignGradeBTN.setFixedSize(180, 60)
        self.assignGradeBTN.setText("Assign Grade")
        self.assignGradeBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.assignGradeBTN)

        self.logoutBTN = QtWidgets.QPushButton()
        self.logoutBTN.setText("Logout")
        self.logoutBTN.setFont(QFont("Century Gothic", 20))
        self.logoutBTN.setFixedSize(180, 60)
        self.logoutBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.logoutBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.logoutBTN)

        self.BTNSW.setLayout(self.BTNSL)

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setFixedHeight(200)
        self.logo.setFixedWidth(200)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.space = QWidget()
        self.space.setFixedHeight(385)

        self.logoL.addWidget(self.logo)
        self.logoL.addWidget(self.space)
        self.logoL.addWidget(self.BTNSW)

        self.logoW.setLayout(self.logoL)
        self.main_contentL.addWidget(self.logoW)
        self.main_contentW.setLayout(self.main_contentL)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked
        self.home.clicked.connect(self.mainpage_home_instructor)
        self.account.clicked.connect(self.mainpage_account_instructor)
        self.logoutBTN.clicked.connect(self.logout)
        self.help.clicked.connect(self.mainpage_help_instructor)
        self.ComplaintBTN.clicked.connect(self.instructor_complaint_page)
        # create new page, 'instructor_complaint_page'
        self.classes.clicked.connect(self.mainpage_classes_instructor)
        self.assignGradeBTN.clicked.connect(self.assign_grade_page)

    def mainpage_account_instructor(self):
        global id
        global acc_type
        global name
        global email
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        self.logOut = QtWidgets.QPushButton()
        self.logOut.setFont(QFont("Century Gothic", 20))
        self.logOut.setFixedSize(180, 60)
        self.logOut.setText("Log out")
        self.logOut.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setFixedHeight(200)
        self.logo.setFixedWidth(200)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.space = QWidget()

        self.logoL.addWidget(self.logo)
        self.logoL.addWidget(self.space)
        self.logoL.addWidget(self.logOut)

        self.logoW.setLayout(self.logoL)
        self.main_contentL.addWidget(self.logoW)

        self.accountDataW = QWidget()
        self.accountDataL = QVBoxLayout()
        self.accountDataL.setAlignment(Qt.AlignHCenter)

        self.accountDataW.setFixedSize(480, 660)
        self.accountDataW.setStyleSheet(
            "border: 1px solid white;border-radius:15px;margin-top:30px;"
        )

        self.accountNameTXT = QtWidgets.QLabel()
        self.accountNameTXT.setText("Account name :")
        self.accountNameTXT.setStyleSheet("color:white; border:0;")
        self.accountNameTXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountNameTXT)

        self.accountName = QtWidgets.QLabel()
        self.accountName.setText(name)
        self.accountName.setStyleSheet("color:#0583F2; border:0;")
        self.accountName.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountName)

        self.email_TXT = QtWidgets.QLabel()
        self.email_TXT.setText("E-mail :")
        self.email_TXT.setStyleSheet("color:white; border:0;")
        self.email_TXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.email_TXT)

        self.email = QtWidgets.QLabel()
        self.email.setText(email)
        self.email.setStyleSheet("color:#0583F2; border:0;")
        self.email.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.email)

        self.idTXT = QtWidgets.QLabel()
        self.idTXT.setText("Student ID :")
        self.idTXT.setStyleSheet("color:white; border:0;")
        self.idTXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.idTXT)

        self.accountId = QtWidgets.QLabel()
        self.accountId.setText(id)
        self.accountId.setStyleSheet("color:#0583F2; border:0;")
        self.accountId.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountId)

        self.accountTypeTXT = QtWidgets.QLabel()
        self.accountTypeTXT.setText("Account type :")
        self.accountTypeTXT.setStyleSheet("color:white; border:0;")
        self.accountTypeTXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountTypeTXT)

        self.accountType = QtWidgets.QLabel()
        self.accountType.setText("Instructor")
        self.accountType.setStyleSheet("color:#0583F2; border:0;")
        self.accountType.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountType)

        self.accountDataW.setLayout(self.accountDataL)
        self.main_contentL.addWidget(self.accountDataW)
        self.main_contentW.setLayout(self.main_contentL)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.home.clicked.connect(self.mainpage_home_instructor)
        self.account.clicked.connect(self.mainpage_account_instructor)
        self.help.clicked.connect(self.mainpage_help_instructor)
        self.logOut.clicked.connect(self.logout)
        self.classes.clicked.connect(self.mainpage_classes_instructor)

    def mainpage_help_instructor(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        self.BTNSW = QWidget()
        self.BTNSL = QHBoxLayout()

        # self.logoutBTN = QtWidgets.QPushButton()
        # self.logoutBTN.setText("Back")
        # self.logoutBTN.setFont(QFont("Century Gothic", 20))
        # self.logoutBTN.setFixedSize(180, 60)
        # self.logoutBTN.setCursor(QCursor(Qt.PointingHandCursor))
        # self.logoutBTN.setStyleSheet(
        #    "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
        #    "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        # )
        # self.BTNSL.addWidget(self.logoutBTN)

        self.BTNSW.setLayout(self.BTNSL)

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setFixedHeight(200)
        self.logo.setFixedWidth(200)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.space = QWidget()
        self.space.setFixedHeight(385)

        self.logoL.addWidget(self.logo)
        self.logoL.addWidget(self.space)
        self.logoL.addWidget(self.BTNSW)

        self.logoW.setLayout(self.logoL)
        self.main_contentL.addWidget(self.logoW)
        self.main_contentW.setLayout(self.main_contentL)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)
        # -------------End of Design-------------

        # scroll settingsx
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.home.clicked.connect(self.mainpage_home_instructor)
        self.account.clicked.connect(self.mainpage_account_instructor)
        self.help.clicked.connect(self.mainpage_help_instructor)
        self.classes.clicked.connect(self.mainpage_classes_instructor)
        # self.logoutBTN.clicked.connect(self.startup_page)

    def mainpage_classes_instructor(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QVBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        # self.BTNSW = QWidget()
        # self.BTNSL = QHBoxLayout()

        # self.backToStartupBTN = QtWidgets.QPushButton()
        # self.backToStartupBTN.setText("Back")
        # self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        # self.backToStartupBTN.setFixedSize(180, 60)
        # self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        # self.backToStartupBTN.setStyleSheet(
        #     "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
        #     "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        # )
        # self.BTNSL.addWidget(self.backToStartupBTN)

        # self.BTNSW.setLayout(self.BTNSL)

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setFixedHeight(200)
        self.logo.setFixedWidth(200)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.space = QWidget()
        self.space.setFixedHeight(85)

        self.logoL.addWidget(self.logo)
        self.logoL.addWidget(self.space)

        self.logoW.setLayout(self.logoL)
        # self.main_contentL.addWidget(self.logoW)
        self.main_contentW.setLayout(self.main_contentL)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.home.clicked.connect(self.mainpage_home_instructor)
        self.account.clicked.connect(self.mainpage_account_instructor)
        self.help.clicked.connect(self.mainpage_help_instructor)
        self.classes.clicked.connect(self.mainpage_classes_instructor)
        # self.backToStartupBTN.clicked.connect(self.StartupStudent)

    def set_period(self):
        period_name = self.periods.currentText()
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        if period_name == "class_set_up":
            c.execute("UPDATE periods SET current_period = 0")
            conn.commit()
            conn.close()
        elif period_name == "course_registration":
            c.execute("UPDATE periods SET current_period = 1")
            conn.commit()
            conn.close()
        elif period_name == "class_running":
            c.execute("UPDATE periods SET current_period = 2")
            conn.commit()
            conn.close()
        elif period_name == "grading":
            c.execute("UPDATE periods SET current_period = 3")
            conn.commit()
            conn.close()
        elif period_name == "post-grading":
            c.execute("UPDATE periods SET current_period = 4")
            conn.commit()
            conn.close()

    def mainpage_home_registrar(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        self.BTNSW = QWidget()
        self.BTNSL = QHBoxLayout()

        self.ComplaintBTN = QtWidgets.QPushButton()
        self.ComplaintBTN.setFont(QFont("Century Gothic", 20))
        self.ComplaintBTN.setFixedSize(180, 60)
        self.ComplaintBTN.setText("Complaint")
        self.ComplaintBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.ComplaintBTN)

        self.applicationsBTN = QtWidgets.QPushButton()  # Aiman 11/6
        self.applicationsBTN.setFont(QFont("Century Gothic", 17))
        self.applicationsBTN.setFixedSize(180, 60)
        self.applicationsBTN.setText("Applications")
        self.applicationsBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.applicationsBTN)

        # Start
        self.ReviewRegistrarBTN = QtWidgets.QPushButton()
        self.ReviewRegistrarBTN.setText("Review")
        self.ReviewRegistrarBTN.setFont(QFont("Century Gothic", 20))
        self.ReviewRegistrarBTN.setFixedSize(180, 60)
        self.ReviewRegistrarBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.ReviewRegistrarBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.ReviewRegistrarBTN)
        # End

        # Start
        self.issuewarningBTN = QtWidgets.QPushButton()
        self.issuewarningBTN.setText("Manage")
        self.issuewarningBTN.setFont(QFont("Century Gothic", 20))
        self.issuewarningBTN.setFixedSize(180, 60)
        self.issuewarningBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.issuewarningBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.issuewarningBTN)
        # End

        self.logoutBTN = QtWidgets.QPushButton()
        self.logoutBTN.setText("Logout")
        self.logoutBTN.setFont(QFont("Century Gothic", 20))
        self.logoutBTN.setFixedSize(180, 60)
        self.logoutBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.logoutBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.logoutBTN)

        self.BTNSW.setLayout(self.BTNSL)

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setFixedHeight(200)
        self.logo.setFixedWidth(200)
        self.logo.setPixmap(QPixmap("logo.png"))

        self.periods = QtWidgets.QComboBox()
        self.periods.setFont(QFont("Century Gohic", 16))
        self.periods.setFixedSize(400, 40)
        self.periods.addItem("class_set_up")
        self.periods.addItem("course_registration")
        self.periods.addItem("class_running")
        self.periods.addItem("grading")
        self.periods.addItem("post-grading")
        self.periods.setStyleSheet(comboBox_stylesheet)
        self.space = QWidget()
        self.space.setFixedHeight(260)

        self.confirmBTN = QtWidgets.QPushButton()
        self.confirmBTN.setFont(QFont("Century Gothic", 20))
        self.confirmBTN.setFixedSize(180, 60)
        self.confirmBTN.setText("Confirm")
        self.confirmBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.logoL.addWidget(self.logo)
        self.logoL.addWidget(self.periods)
        self.logoL.addWidget(self.confirmBTN)
        self.logoL.addWidget(self.space)
        self.logoL.addWidget(self.BTNSW)

        self.logoW.setLayout(self.logoL)
        self.main_contentL.addWidget(self.logoW)
        self.main_contentW.setLayout(self.main_contentL)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked
        self.home.clicked.connect(self.mainpage_home_registrar)
        self.applicationsBTN.clicked.connect(self.applications)  # Aiman 11/6
        self.account.clicked.connect(self.mainpage_account_registrar)
        self.logoutBTN.clicked.connect(self.startup_page)
        self.help.clicked.connect(self.mainpage_help_registrar)
        self.ComplaintBTN.clicked.connect(self.complaint_page_registrar)
        self.classes.clicked.connect(self.mainpage_classes_registrar)
        self.ReviewRegistrarBTN.clicked.connect(self.review_page_registrar)
        self.issuewarningBTN.clicked.connect(self.issuewarning_page_registrar)
        self.confirmBTN.clicked.connect(self.set_period)
        # self.sssssBTN.clicked.connect(self.issuewarning_page_registrar)

    # Aiman test

    def mainpage_account_registrar(self):
        global id
        global acc_type
        global name
        global email
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        self.logOut = QtWidgets.QPushButton()
        self.logOut.setFont(QFont("Century Gothic", 20))
        self.logOut.setFixedSize(180, 60)
        self.logOut.setText("Log out")
        self.logOut.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setFixedHeight(200)
        self.logo.setFixedWidth(200)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.space = QWidget()

        self.logoL.addWidget(self.logo)
        self.logoL.addWidget(self.space)
        self.logoL.addWidget(self.logOut)

        self.logoW.setLayout(self.logoL)
        self.main_contentL.addWidget(self.logoW)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.main_contentL.addWidget(self.space)

        self.accountDataW = QWidget()
        self.accountDataL = QVBoxLayout()
        self.accountDataL.setAlignment(Qt.AlignHCenter)

        self.accountDataW.setFixedSize(480, 660)
        self.accountDataW.setStyleSheet(
            "border: 1px solid white;border-radius:15px;margin-top:30px;"
        )

        self.accountNameTXT = QtWidgets.QLabel()
        self.accountNameTXT.setText("Account name :")
        self.accountNameTXT.setStyleSheet("color:white; border:0;")
        self.accountNameTXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountNameTXT)

        self.accountName = QtWidgets.QLabel()
        self.accountName.setText(name)
        self.accountName.setStyleSheet("color:#0583F2; border:0;")
        self.accountName.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountName)

        self.email_TXT = QtWidgets.QLabel()
        self.email_TXT.setText("E-mail :")
        self.email_TXT.setStyleSheet("color:white; border:0;")
        self.email_TXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.email_TXT)

        self.email = QtWidgets.QLabel()
        self.email.setText(email)
        self.email.setStyleSheet("color:#0583F2; border:0;")
        self.email.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.email)

        self.idTXT = QtWidgets.QLabel()
        self.idTXT.setText("Student ID :")
        self.idTXT.setStyleSheet("color:white; border:0;")
        self.idTXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.idTXT)

        self.accountId = QtWidgets.QLabel()
        self.accountId.setText(id)
        self.accountId.setStyleSheet("color:#0583F2; border:0;")
        self.accountId.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountId)

        self.accountTypeTXT = QtWidgets.QLabel()
        self.accountTypeTXT.setText("Account type :")
        self.accountTypeTXT.setStyleSheet("color:white; border:0;")
        self.accountTypeTXT.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountTypeTXT)

        self.accountType = QtWidgets.QLabel()  # Aiman Why
        self.accountType.setText("Registrar")
        self.accountType.setStyleSheet("color:#0583F2; border:0;")
        self.accountType.setFont(QFont("Century Gothic", 18))

        self.accountDataL.addWidget(self.accountType)

        self.accountDataW.setLayout(self.accountDataL)
        self.main_contentL.addWidget(self.accountDataW)
        self.main_contentW.setLayout(self.main_contentL)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.home.clicked.connect(self.mainpage_home_registrar)
        self.account.clicked.connect(self.mainpage_account_registrar)
        self.help.clicked.connect(self.mainpage_help_registrar)
        self.logOut.clicked.connect(self.logout)
        self.classes.clicked.connect(self.mainpage_classes_registrar)

    def mainpage_help_registrar(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        # self.BTNSW = QWidget()
        # self.BTNSL = QHBoxLayout()

        # self.backToStartupBTN = QtWidgets.QPushButton()
        # self.backToStartupBTN.setText("Back")
        # self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        # self.backToStartupBTN.setFixedSize(180, 60)
        # self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        # self.backToStartupBTN.setStyleSheet(
        #     "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
        #     "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        # )
        # self.BTNSL.addWidget(self.backToStartupBTN)

        # self.BTNSW.setLayout(self.BTNSL)

        # self.logo = QtWidgets.QLabel(self.logoW)
        # self.logo.setFixedHeight(200)
        # self.logo.setFixedWidth(200)
        # self.logo.setPixmap(QPixmap("logo.png"))
        # self.space = QWidget()
        # self.space.setFixedHeight(385)

        # self.logoL.addWidget(self.logo)
        # self.logoL.addWidget(self.space)
        # self.logoL.addWidget(self.BTNSW)

        # self.logoW.setLayout(self.logoL)
        self.main_contentL.addWidget(self.logoW)
        self.main_contentW.setLayout(self.main_contentL)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)
        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.home.clicked.connect(self.mainpage_home_registrar)
        self.account.clicked.connect(self.mainpage_account_registrar)
        self.help.clicked.connect(self.mainpage_help_registrar)
        self.classes.clicked.connect(self.mainpage_classes_registrar)
        # self.backToStartupBTN.clicked.connect(self.mainpage)

    # Start
    def review_page_registrar(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.main_contentW = QWidget()
        self.main_contentL = QVBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        review = sqlite3.connect("gsz.db")
        df = display_db.pd.read_sql_query("SELECT * FROM reviews", review)

        self.model = display_db.pandasModel(df)
        self.view = QTableView()
        self.view.setModel(self.model)
        ids = []
        cboxes = []
        index = 0

        self.view.resize(800, 600)
        self.view.show()

        self.main_contentW.setLayout(self.main_contentL)

        self.back = QtWidgets.QPushButton()
        self.back.setText("Back")
        self.back.setFont(QFont("Century Gothic", 20))
        self.back.setFixedSize(180, 60)
        self.back.setCursor(QCursor(Qt.PointingHandCursor))
        self.back.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.mainL.addWidget(self.back)
        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        # -------------End of Design-------------

        # applicant = sqlite3.connect("gsz.db")
        # df = display_db.pd.read_sql_query("SELECT * FROM applicants", applicant)
        # df = df.drop(["num_courses_taken", "applicant_id"], axis=1)

        # model = display_db.pandasModel(df)
        # view = QTableView()
        # view.setModel(model)
        # view.resize(800, 600)
        # view.show()

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.back.clicked.connect(self.mainpage_home_registrar)

        # End

    def add_classes(self, days):
        global user
        schedule = []
        for day in days:
            tmp = list(map(lambda x: x.currentText(), day[1:6]))
            tmp.append(day[0])
            # print(tmp)
            if tmp[4] == "on":
                schedule.append(tmp)
        starts = [datetime.strptime(x[0] + ":" + x[1], "%H:%M") for x in schedule]
        ends = [datetime.strptime(x[2] + ":" + x[3], "%H:%M") for x in schedule]
        for start, end in zip(starts, ends):

            if start >= end:
                self.dlg = QDialog()
                self.conflict = QtWidgets.QLabel(self.dlg)
                self.conflict.setText("time conflict")
                self.conflict.setFont(QFont("Century Gothic", 10))
                self.conflict.move(10, 10)
        self.b1 = QPushButton("ok", self.dlg)
        self.b1.move(50, 60)
        self.b1.clicked.connect(self.getJustification)
        self.b1.show()
        self.dlg.setWindowTitle("Dialog")
        self.dlg.setWindowModality(Qt.ApplicationModal)
        self.dlg.exec_()

        class_name = self.nameRegistrar.text()
        instructor = self.instructor.currentText()
        seats = self.seats.currentText()
        time = list(
            map(
                lambda x: x[5] + " " + x[0] + ":" + x[1] + " - " + x[2] + ":" + x[3],
                schedule,
            )
        )
        time = str(time).strip("[]").replace("'", "")
        user.course_set_up(class_name, time, self.ins[instructor], seats)
        self.mainpage_home_registrar()

    # def course_set_up(self, name, time, instructor, size):
    # instructor1 = Instructor(args[0])
    # reg1.course_set_up("CSC 33500", "Tu 12:00 - 1:15, We 12:00 - 2:30", args[0], 25)

    def mainpage_classes_registrar(self):
        global comboBox_stylesheet
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.account = QtWidgets.QPushButton()
        self.account.setFixedSize(310, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(310, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(310, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.classes = QtWidgets.QPushButton()
        self.classes.setFixedSize(310, 60)
        self.classes.setCursor(QCursor(Qt.PointingHandCursor))
        self.classes.setText("Classes")
        self.classes.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.classes.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.classes)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QVBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        self.BTNSW = QWidget()
        self.BTNSL = QHBoxLayout()

        # self.backToStartupBTN = QtWidgets.QPushButton()
        # self.backToStartupBTN.setText("Back")
        # self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        # self.backToStartupBTN.setFixedSize(180, 60)
        # self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        # self.backToStartupBTN.setStyleSheet(
        #     "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
        #     "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        # )
        # self.BTNSL.addWidget(self.backToStartupBTN)

        # self.BTNSW.setLayout(self.BTNSL)

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setFixedHeight(200)
        self.logo.setFixedWidth(200)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.space = QWidget()
        self.space.setFixedHeight(85)

        self.logoL.addWidget(self.logo)
        self.logoL.addWidget(self.space)

        self.logoW.setLayout(self.logoL)
        # self.main_contentL.addWidget(self.logoW)
        self.main_contentW.setLayout(self.main_contentL)

        self.nameRegistrarTXT = QtWidgets.QLabel()
        self.nameRegistrarTXT.setText("Name :")
        self.nameRegistrarTXT.setStyleSheet("color:white;padding-bottom:10px;")
        self.nameRegistrarTXT.setFont(QFont("Century Gothic", 20))

        self.nameRegistrar = QtWidgets.QLineEdit()
        self.nameRegistrar.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.nameRegistrar.setFont(QFont("Century Gothic", 16))
        self.nameRegistrar.setFixedSize(400, 40)

        self.instructorTXT = QtWidgets.QLabel()
        self.instructorTXT.setText("Instructor :")
        self.instructorTXT.setStyleSheet("color:white;padding-bottom:10px;")
        self.instructorTXT.setFont(QFont("Century Gothic", 20))

        self.instructor = QtWidgets.QComboBox()
        self.instructor.setStyleSheet(comboBox_stylesheet)
        self.instructor.setFont(QFont("Century Gothic", 16))
        self.instructor.setFixedSize(400, 40)

        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "SELECT first, last, user_id FROM users WHERE user_type = ?"
        c.execute(sql, ("instructor",))
        instructor_names = c.fetchall()
        # print(instructor_names)
        self.ins = {
            instructor_name[0] + " " + instructor_name[1]: instructor_name[2]
            for instructor_name in instructor_names
        }
        # a = [
        #     ("Michael", "Jordan", 9),
        #     ("Jane", "Doe", 10),
        #     ("Jane", "Doe", 14),
        #     ("Jane", "Doe", 18),
        #     ("James", "Milner", 19),
        # ]
        # dic = {ai[0] + " " + ai[1]: ai[2] for ai in a}
        # print(dic)

        for instructor_name in instructor_names:
            self.instructor.addItem(instructor_name[0] + " " + instructor_name[1])

        self.seatsTXT = QtWidgets.QLabel()
        self.seatsTXT.setText("Seats :")
        self.seatsTXT.setStyleSheet("color:white;padding-bottom:10px;")
        self.seatsTXT.setFont(QFont("Century Gothic", 20))

        self.seats = QtWidgets.QComboBox()
        self.seats.setStyleSheet(comboBox_stylesheet)
        self.seats.setFont(QFont("Century Gothic", 16))
        self.seats.setFixedSize(400, 40)
        self.seats.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(11):
            self.seats.addItem(str(f"  {i+5}"))

        # self.scheduleTXT = QtWidgets.QLabel()
        # self.scheduleTXT.setText("Schedule :")
        # self.scheduleTXT.setStyleSheet("color:white;padding-bottom:10px;")
        # self.scheduleTXT.setFont(QFont("Century Gothic", 20))

        schedule = sqlite3.connect("gsz.db")
        df = display_db.pd.read_sql_query("SELECT * FROM schedule", schedule)
        self.model = display_db.pandasModel(df)
        self.view = QTableView()
        self.view.setModel(self.model)
        mo, tu, we, th, fr = ["Mo"], ["Tu"], ["We"], ["Th"], ["Fr"]
        for index, row in df.iterrows():
            # print(row)
            for i in range(1, 5):
                c = QComboBox()
                if i % 2 == 1:
                    c.addItems(list(map(lambda x: str(x), list(range(8, 21)))))
                else:
                    c.addItems(list(map(lambda x: str(x), list(range(15, 56, 15)))))
                x = self.view.model().index(index, i)
                self.view.setIndexWidget(x, c)
                if row[0] == "Mo":
                    mo.append(c)
                elif row[0] == "Tu":
                    tu.append(c)
                elif row[0] == "We":
                    we.append(c)
                elif row[0] == "Th":
                    th.append(c)
                else:
                    fr.append(c)
            c = QComboBox()
            if row[0] == "Mo":
                mo.append(c)
            elif row[0] == "Tu":
                tu.append(c)
            elif row[0] == "We":
                we.append(c)
            elif row[0] == "Th":
                th.append(c)
            else:
                fr.append(c)
            c.addItems(["off", "on"])
            x = self.view.model().index(index, 5)
            self.view.setIndexWidget(x, c)
        self.view.resize(800, 600)
        self.view.show()

        days = [mo, tu, we, th, fr]

        self.registerBTN = QtWidgets.QPushButton()
        self.registerBTN.setText("Register")
        self.registerBTN.setFont(QFont("Century Gothic", 20))
        self.registerBTN.setFixedSize(180, 60)
        self.registerBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.registerBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.main_contentL.addWidget(self.nameRegistrarTXT)
        self.main_contentL.addWidget(self.nameRegistrar)
        self.main_contentL.addWidget(self.instructorTXT)
        self.main_contentL.addWidget(self.instructor)
        self.main_contentL.addWidget(self.seatsTXT)
        self.main_contentL.addWidget(self.seats)
        # self.main_contentL.addWidget(self.scheduleTXT)
        # self.main_contentL.addWidget(self.mondayW)
        # self.main_contentL.addWidget(self.tuesdayW)
        # self.main_contentL.addWidget(self.wednesdayW)
        # self.main_contentL.addWidget(self.thursdayW)
        # self.main_contentL.addWidget(self.fridayW)
        self.main_contentL.addWidget(self.registerBTN)

        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.home.clicked.connect(self.mainpage_home_registrar)
        self.account.clicked.connect(self.mainpage_account_registrar)
        self.help.clicked.connect(self.mainpage_help_registrar)
        self.classes.clicked.connect(self.mainpage_classes_registrar)
        self.registerBTN.clicked.connect(lambda: self.add_classes(days))

        # self.backToStartupBTN.clicked.connect(self.StartupStudent)

        # Aiman 11/6

    def addClass(self, addBtn):
        # change this if statement to If the class is actually added or not
        global user
        class_name = self.className.text()
        print(class_name)
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "SELECT course_id from courses WHERE course_name = ?"
        c.execute(sql, (class_name,))
        course_id = c.fetchone()[0]
        result = user.enroll_course(course_id)
        if result == 1:
            addBtn.setText("Added")
            addBtn.setStyleSheet(
                "QPushButton{background-color:#4FE80C;border-radius: 10px;color: white;}"
                "QPushButton:pressed{background-color: #3bad09;border-style: inset;}"
            )
        else:
            addBtn.setText("Denied")
            addBtn.setStyleSheet(
                "QPushButton{background-color:#e80909;border-radius: 10px;color: white;}"
                "QPushButton:pressed{background-color: #b30707;border-style: inset;}"
            )

    def getJustification(self):
        justification = self.justify_entry.text()
        self.filePath = justification
        self.dlg.accept()

    def justification(self, msg):
        self.filePath = None
        self.dlg = QDialog()
        self.justify = QtWidgets.QLabel(self.dlg)
        self.justify.setText(msg)
        self.justify.setFont(QFont("Century Gothic", 10))
        self.justify.move(10, 10)
        self.justify_entry = QtWidgets.QLineEdit(self.dlg)
        self.justify_entry.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.justify_entry.setFont(QFont("Century Gothic", 16))
        self.justify_entry.setFixedSize(150, 17)
        self.justify_entry.move(20, 30)

        self.b1 = QPushButton("submit", self.dlg)
        self.b1.move(50, 60)
        self.b1.clicked.connect(self.getJustification)
        self.b1.show()
        self.dlg.setWindowTitle("Dialog")
        self.dlg.setWindowModality(Qt.ApplicationModal)
        self.dlg.exec_()

    def submit_application(self, ids, decisions):
        decisions = list(map(lambda x: x.currentText(), decisions))
        global user
        conn = sqlite3.connect("gsz.db")
        for id, decision in zip(ids, decisions):
            if user.is_valid_applicant(id) and (decision == "deny"):
                conn = sqlite3.connect("gsz.db")
                c = conn.cursor()
                sql = "SELECT first, last, GPA FROM applicants WHERE applicant_id = ?"
                c.execute(sql, (id,))
                app_info = c.fetchone()
                msg = f"Why? {app_info[0]} {app_info[1]}'s GPA is {app_info[2]}?"
                self.justification(msg)
                user.email_result(id, decision, self.justification)
            else:
                user.email_result(id, decision, None)
        self.mainpage_home_registrar()

    def applications(self):
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        # ----------------Design-----------------

        self.main_contentW = QWidget()
        self.main_contentL = QVBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()
        self.logoL = QVBoxLayout()
        self.logoL.setContentsMargins(0, 0, 0, 0)

        self.BTNSW = QWidget()
        self.BTNSL = QHBoxLayout()

        self.backToHomeBTN = QtWidgets.QPushButton()
        self.backToHomeBTN.setText("back")
        self.backToHomeBTN.setFont(QFont("Century Gothic", 20))
        self.backToHomeBTN.setFixedSize(180, 60)
        self.backToHomeBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToHomeBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToHomeBTN)

        self.BTNSW.setLayout(self.BTNSL)

        self.submitBTN = QtWidgets.QPushButton()
        self.submitBTN.setText("Submit")
        self.submitBTN.setFont(QFont("Century Gothic", 20))
        self.submitBTN.setFixedSize(180, 60)
        self.submitBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.submitBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.submitBTN)

        self.BTNSW.setLayout(self.BTNSL)

        applicant = sqlite3.connect("gsz.db")
        df = display_db.pd.read_sql_query("SELECT * FROM applicants", applicant)
        df = df.drop(["num_courses_taken"], axis=1)
        self.model = display_db.pandasModel(df)
        self.view = QTableView()
        self.view.setModel(self.model)
        ids = []
        cboxes = []
        index = 0
        for row in df["applicant_id"]:
            ids.append(row)
            c = QComboBox()
            c.addItems(["deny", "approve"])
            x = self.view.model().index(index, 7)
            self.view.setIndexWidget(x, c)
            cboxes.append(c)
            index += 1
        self.view.resize(800, 600)
        self.view.show()
        # worning or deregister
        # self.logo = QtWidgets.QLabel(self.logoW)
        # self.logo.setFixedHeight(200)
        # self.logo.setFixedWidth(200)
        # self.logo.setPixmap(QPixmap("logo.png"))
        # self.space = QWidget()
        # self.space.setFixedHeight(85)

        # self.logoL.addWidget(self.logo)
        # self.logoL.addWidget(self.space)

        # self.logoW.setLayout(self.logoL)
        # self.main_contentL.addWidget(self.logoW)
        self.main_contentW.setLayout(self.main_contentL)

        # ------------------------start-----------------------------
        # try:
        #     global applications

        #     self.applicationsW = QWidget()
        #     self.applicationsL = QVBoxLayout()

        #     for i in applications:
        #         self.StudentClassW = QtWidgets.QWidget()
        #         self.StudentClassW.setStyleSheet(
        #             "background-color:white;border-radius:15px;"
        #         )
        #         self.StudentClassL = QHBoxLayout()

        #         self.firstName = QtWidgets.QLabel()
        #         self.firstName.setFixedWidth(180)
        #         self.firstName.setText(f"First name:\n\n{i[0]}")
        #         self.firstName.setFont(QFont("Century Gothic", 10))

        #         self.secondName = QtWidgets.QLabel()
        #         self.secondName.setText(f"Second name:\n\n{i[1]}")
        #         self.secondName.setFont(QFont("Century Gothic", 10))

        #         self.email = QtWidgets.QLabel()
        #         self.email.setText(f"E-mail:\n\n{i[2]}")
        #         self.email.setFont(QFont("Century Gothic", 10))

        #         self.GPA = QtWidgets.QLabel()
        #         self.GPA.setText(f"GPA:\n\n{i[3]}")
        #         self.GPA.setFont(QFont("Century Gothic", 10))

        #         self.resume = QtWidgets.QLabel()
        #         self.resume.setText(f"Resume:\n\n{i[4]}")
        #         self.resume.setFont(QFont("Century Gothic", 10))

        #         self.userType = QtWidgets.QLabel()
        #         self.userType.setText(f"User type:\n\n{i[5]}")
        #         self.userType.setFont(QFont("Century Gothic", 10))

        #         self.approveBTN = QtWidgets.QPushButton()
        #         self.approveBTN.setText("Approve")
        #         self.approveBTN.setFont(QFont("Century Gothic", 8))
        #         self.approveBTN.setFixedSize(70, 40)
        #         self.approveBTN.setStyleSheet(
        #             "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
        #             "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        #         )

        #         self.denyBTN = QtWidgets.QPushButton()
        #         self.denyBTN.setText("Deny")
        #         self.denyBTN.setFont(QFont("Century Gothic", 8))
        #         self.denyBTN.setFixedSize(70, 40)
        #         self.denyBTN.setStyleSheet(
        #             "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
        #             "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        #         )

        #         space = QWidget()
        #         space.setFixedWidth(20)

        #         self.StudentClassL.addWidget(self.firstName)
        #         self.StudentClassL.addWidget(self.secondName)
        #         self.StudentClassL.addWidget(self.email)
        #         self.StudentClassL.addWidget(self.GPA)
        #         self.StudentClassL.addWidget(self.resume)
        #         self.StudentClassL.addWidget(self.userType)
        #         self.StudentClassL.addWidget(space)
        #         self.StudentClassL.addWidget(self.approveBTN)
        #         self.StudentClassL.addWidget(self.denyBTN)

        #         self.StudentClassW.setLayout(self.StudentClassL)
        #         self.applicationsL.addWidget(self.StudentClassW)

        #     self.applicationsW.setLayout(self.applicationsL)
        #     self.main_contentL.addWidget(self.applicationsW)
        # except Exception as e:
        #     print(e)

        # -------------------------end------------------------------

        self.mainL.addWidget(self.backToHomeBTN)
        self.mainL.addWidget(self.submitBTN)
        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        # applicant = sqlite3.connect("gsz.db")
        # df = display_db.pd.read_sql_query("SELECT * FROM applicants", applicant)
        # df = df.drop(["num_courses_taken", "applicant_id"], axis=1)

        # model = display_db.pandasModel(df)
        # view = QTableView()
        # view.setModel(model)
        # view.resize(800, 600)
        # view.show()

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.backToHomeBTN.clicked.connect(self.mainpage_home_registrar)
        self.submitBTN.clicked.connect(lambda: self.submit_application(ids, cboxes))

        # Aiman 11/6 end

    def logout(self):
        name = ""
        email = ""
        acc_type = ""
        id = ""
        self.startup_page()  # Aiman last change

    def getNewPass(self):
        global user
        newPassword = self.newPassword_entry.text()
        user.update_first_login()
        user.change_password(newPassword)
        self.dlg.accept()

    def newPass(self):
        self.filePath = None
        self.dlg = QDialog()
        self.newPassword = QtWidgets.QLabel(self.dlg)
        self.newPassword.setText("type your new password")
        self.newPassword.setFont(QFont("Century Gothic", 10))
        self.newPassword.move(10, 10)
        self.newPassword_entry = QtWidgets.QLineEdit(self.dlg)
        self.newPassword_entry.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.newPassword_entry.setFont(QFont("Century Gothic", 16))
        self.newPassword_entry.setFixedSize(150, 17)
        self.newPassword_entry.move(20, 30)
        self.b1 = QPushButton("confirm", self.dlg)
        self.b1.move(50, 60)
        self.b1.clicked.connect(self.getNewPass)
        self.b1.show()
        self.dlg.setWindowTitle("new password")
        self.dlg.setWindowModality(Qt.ApplicationModal)
        self.dlg.exec_()

    def login(self):
        global user, name, email, id
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE id=? AND password=?",
            (self.idBOX.text(), self.passwordBOX.text()),
        )
        row = c.fetchone()
        if row != None:
            name = f"{row[1]} {row[2]}"
            email = str(row[5])
            id = str(row[3])
            # checking if it is a first login
            if row[7] == 1:
                # pop up window for setting up a new password
                # new_password = get from gui
                # user.change_password(new_password)
                user = User(row[0])
                self.newPass()
            # create instance of user
            if row[6] == "student":
                user = Student(row[0])
                if get_current_period()==4: # period is poast grade
                    user.end_of_year_student()
                self.mainpage_home_student()
            elif row[6] == "instructor":
                user = Instructor(row[0])
                if get_current_period()==4:
                    user.end_of_year_instructor()              
                self.mainpage_home_instructor()
            else:
                user = Registrar(row[0])
                self.mainpage_home_registrar()
        conn.close()
        self.tipsTXT.setText(
            "\n\n\n\n\n          Invalid user\n   Sign in to create an \n            account"
        )


# users table
conn = sqlite3.connect("gsz.db")
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS users (
        user_id integer PRIMARY KEY,
        first text NOT NULL,
        last text NOT NULL,
        id text NOT NULL,
        password text NOT NULL,
        email text NOT NULL,
        user_type text NOT NULL,
        first_login integer NOT NULL)
        """
)
c.execute("SELECT user_id FROM users LIMIT 1")
if c.fetchall() == []:
    many_registrars = [
        ("Jaehong", "Cho", "id1", "123", "email@email.com", "registrar", 0),
        ("Aiman", "Last", "id2", "123", "email@email.com", "registrar", 0),
        ("Ragib", "Last", "id3", "123", "email@email.com", "registrar", 0),
        ("Michael", "Last", "id4", "123", "email@email.com", "registrar", 0),
        ("Joel", "Last", "id5", "123", "email@email.com", "registrar", 0),
    ]
    c.executemany(
        """INSERT INTO users(first, last, id, password, email, user_type, first_login) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        many_registrars,
    )
conn.commit()

# applicants table
c.execute(
    """CREATE TABLE IF NOT EXISTS applicants(
        applicant_id integer PRIMARY KEY,
        first text NOT NULL,
        last text NOT NULL,
        email text NOT NULL,
        gpa real,
        resume text,
        num_courses_taken integer,
        user_type text NOT NULL,
        approval_status text NOT NULL
        )"""
)
conn.commit()

# students table
c.execute(
    """CREATE TABLE IF NOT EXISTS students (
        student_id integer PRIMARY KEY,
        user_id integer NOT NULL,
        gpa real NOT NULL,
        num_courses_taken integer NOT NULL,
        honor_count integer NOT NULL,
        warning_count integer NOT NULL,
        semester_gpa real,
        is_suspended text DEFAULT False,
        apply_graduate text DEFAULT False,
        degree text DEFAULT Undergrads,
        FOREIGN KEY ('user_id') REFERENCES users (user_id)
        )"""
)
conn.commit()

# instructors table
c.execute(
    """CREATE TABLE IF NOT EXISTS instructors (
        instructor_id integer PRIMARY KEY,
        user_id integer NOT NULL,
        warning_count integer NOT NULL,
        is_suspended integer NOT NULL,
        FOREIGN KEY ('user_id') REFERENCES users (user_id)
        )"""
)
conn.commit()

# courses table
c.execute(
    """CREATE TABLE IF NOT EXISTS courses (
        course_id integer PRIMARY KEY,
        course_name text NOT NULL,
        course_rating real,
        course_time text NOT NULL,
        instructor_id integer NOT NULL,
        course_size integer NOT NULL,
        enroll_count integer,
        course_gpa real,
        is_fair text DEFAULT True,
        FOREIGN KEY ('instructor_id') REFERENCES users (user_id)
        )"""
)

# enrollments table
c.execute(
    """CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id integer PRIMARY KEY,
        student_id integer NOT NULL,
        course_id integer NOT NULL,
        grade real,
        FOREIGN KEY ('student_id') REFERENCES students (student_id),
        FOREIGN KEY ('course_id') REFERENCES courses (course_id)
        )"""
)
conn.commit()

# course_historys table
c.execute(
    """CREATE TABLE IF NOT EXISTS course_historys (
        course_history_id integer PRIMARY KEY,
        student_id integer NOT NULL,
        course_id integer NOT NULL,
        grade real,
        FOREIGN KEY ('student_id') REFERENCES students (student_id),
        FOREIGN KEY ('course_id') REFERENCES courses (course_id)
        )"""
)
conn.commit()

# waitlists table
c.execute(
    """CREATE TABLE IF NOT EXISTS waitlists (
        waitlist_id integer PRIMARY KEY,
        student_id integer NOT NULL,
        course_id integer NOT NULL,
        FOREIGN KEY ('student_id') REFERENCES students (student_id),
        FOREIGN KEY ('course_id') REFERENCES courses (course_id)
        )"""
)
conn.commit()

# complaints table
c.execute(
    """CREATE TABLE IF NOT EXISTS complaints (
        complaint_id integer PRIMARY KEY,
        complainant_id integer NOT NULL,
        complainee_id integer NOT NULL,
        description text NOT NULL,
        complaint_type text,
        FOREIGN KEY ('complainant_id') REFERENCES users (user_id),
        FOREIGN KEY ('complainee_id') REFERENCES users (user_id)
        )"""
)
conn.commit()

# schedule table
c.execute(
    """CREATE TABLE IF NOT EXISTS schedule(
        date text NOT NULL,
        start_hour text,
        start_min text,
        end_hour text,
        end_min text,
        'off/on' text
        )"""
)
c.execute("SELECT date FROM schedule LIMIT 1")
if c.fetchall() == []:
    many_days = [
        ("Mo",),
        ("Tu",),
        ("We",),
        ("Th",),
        ("Fr",),
    ]
    c.executemany(
        "INSERT INTO schedule(date) VALUES(?)",
        many_days,
    )
conn.commit()

# periods table
c.execute(
    """CREATE TABLE IF NOT EXISTS periods(
        period_id integer PRIMARY KEY,
        current_period integer NOT NULL )"""
)
if c.fetchone() == None:
    c.execute("INSERT into periods (current_period) VALUES (0) ")
conn.commit()
conn.close()

##
# # sql = """UPDATE applicants SET first = ?, last = ? WHERE applicant_id = ?"""
# sql = "INSERT INTO schedule(date) VALUES(?)"
# c.execute(sql, ("Mo",))
# c.execute(sql, ("Tu",))
# c.execute(sql, ("We",))
# c.execute(sql, ("Th",))
# c.execute(sql, ("Fr",))

# Running the Gui with the run of application
app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec_()

# plan
# buttons always exist, but if you are in the right period, they will function as they should,
# if you are not, they won't function and give you warning messages
# # use schedule module to play with buttons
