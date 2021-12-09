import sys
import csv
import os
import random
import string
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QCursor, QRegExpValidator

name = ""
email = ""
acc_type = ""
id = ""


class mainWindow(QMainWindow):
    # the innit function with main app attributes
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setWindowTitle("Class Reviews")
        self.setFixedSize(1260, 800)
        self.add_review_page()

    def startup_page(self):
        self.setStyleSheet("background-color:#031926;")
        # main layout and widget
        self.scroll = QtWidgets.QScrollArea()
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()
        self.submitBTN = QtWidgets.QPushButton()
        self.submitBTN.setText("Sign Up")
        self.submitBTN.setFont(QFont("Century Gothic", 20))
        self.submitBTN.setFixedSize(180, 60)
        self.submitBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.submitBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.space = QWidget()
        self.space.setFixedWidth(50)

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
            "\nA student who is in class can write reviews of this case and assign stars (1 worst to 5 best), which will be summarized in the class, no one else except the registrars know who rated which class. The instructor of any course receiving average rating <2 will be warned. An instructor who accumulated 3 warnings will be suspended. The student cannot rate the class after the instructor post the grade. Reviews with 1 or 2 taboo words (the list of taboo words are set up by registrars) will be shown but those words are changed to * and the author receives one warning; whereas reviews with >=3 taboo’s words are not shown in the systems and the author will receive 2 warnings."
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
        # self.submitBTN.clicked.connect(self.add_review_page)
        self.submitFBTN.clicked.connect(self.add_review)

    def add_review(self):
        global id
        global acc_type
        global name
        global email

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
                str(self.ratingBOX.text()),
                str(self.reviewBOX.text().upper()),
            ),
        )

        conn.commit()
        conn.close()



        
        self.check_taboo(self.reviewBOX.text().upper())
        self.close()

    def check_taboo(review):
        
        with open("taboolist.txt") as f:
            lines = f.readlines()

        for line in lines:
            for l in line:
                if l in review:
                    taboo_word = toAsterisk(l)
                    conn = sqlite3.connect("reviews.db")
                    c = conn.cursor()
                    c.execute(
                        """
                                UPDATE reviews
                                SET Review = taboo_word
                                WHERE review_id = row[0]"""
                    )
                    
        conn.commit()
        conn.close()

    def toAsterisk(word):
        stars = "*" * len(word)
        word = stars
        return word

    def calculate_average_rating(self):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(''' SELECT avg(Rating) From reviews WHERE course_id : course_id ''',
                                {'course_id': self.courseidTXT})
        course_rating = c.fetchone()[0]
        c.execute(""" UPDATE courses SET course_rating = :course_rating
                                WHERE course_id = course_id """,
                    {'course_id': self.course_id, 'course_rating' : course_rating})
        conn.commit()
        c.close()

    def receive_warning_instructor(instructor_id):
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

    def receive_warning_std(student_id):
        conn = sqlite3.connect("student.db")
        c = conn.cursor()

        c.execute(
            "SELECT warning_count from students where student_id = :student_id",
            {"student_id": student_id},
        )
        new_warning_count = c.fetchone()[0] + 1

        c.execute(
            """UPDATE student SET warning_count = :new_warning_count
                        WHERE student_id =:student_id""",
            {"student_id": student_id, "new_warning_count": new_warning_count},
        )

        conn.commit()
        conn.close()


# Running the Gui with the run of application
app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec_()
