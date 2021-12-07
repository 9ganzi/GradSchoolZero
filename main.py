import sqlite3

# import task5
import display_db
import sys
import csv
import os
from user import Registrar, Student, Instructor, generate_random
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
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QCursor, QRegExpValidator
from functools import partial  # Aiman 11/6


name = ""
email = ""
acc_type = ""
id = ""
loginState = ""  # Aiman

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
    "selection-color: black;"
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


class mainWindow(QMainWindow):
    # the innit function with main app attributes
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setWindowTitle("Collage App")
        self.setFixedSize(1260, 800)
        self.StartupStudent()

    def StartupStudent(self):
        global loginState
        loginState = "Student"
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.studentPage = QtWidgets.QPushButton()
        self.studentPage.setFixedSize(410, 60)
        self.studentPage.setText("Student")
        self.studentPage.setCursor(QCursor(Qt.PointingHandCursor))
        self.studentPage.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.studentPage.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.studentPage)

        self.InstructorPage = QtWidgets.QPushButton()
        self.InstructorPage.setFixedSize(410, 60)
        self.InstructorPage.setCursor(QCursor(Qt.PointingHandCursor))
        self.InstructorPage.setText("Instructor")
        self.InstructorPage.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.InstructorPage.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.InstructorPage)

        self.RegistrarsPage = QtWidgets.QPushButton()
        self.RegistrarsPage.setFixedSize(410, 60)
        self.RegistrarsPage.setCursor(QCursor(Qt.PointingHandCursor))
        self.RegistrarsPage.setText("Registrars")
        self.RegistrarsPage.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.RegistrarsPage.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.RegistrarsPage)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.stBTNS = QWidget()
        self.stBTNSL = QHBoxLayout()

        self.newStudentBTN = QtWidgets.QPushButton()
        self.newStudentBTN.setText("New student")
        self.newStudentBTN.setFont(QFont("Century Gothic", 26))
        self.newStudentBTN.setFixedSize(380, 90)
        self.newStudentBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.newStudentBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.stBTNSL.addWidget(self.newStudentBTN)

        self.existingStudentBTN = QtWidgets.QPushButton()
        self.existingStudentBTN.setText("Existing student")
        self.existingStudentBTN.setFont(QFont("Century Gothic", 26))
        self.existingStudentBTN.setFixedSize(380, 90)
        self.existingStudentBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.existingStudentBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.stBTNSL.addWidget(self.existingStudentBTN)

        self.stBTNS.setLayout(self.stBTNSL)
        self.mainL.addWidget(self.stBTNS)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        self.existingStudentBTN.clicked.connect(self.startup_page_instructor)
        self.RegistrarsPage.clicked.connect(self.StartupRegistrars)
        self.newStudentBTN.clicked.connect(self.studentDetails)
        self.InstructorPage.clicked.connect(self.StartupInstructor)
        # self.startup_page()

    def StartupInstructor(self):
        global loginState
        loginState = "Instructor"
        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.studentPage = QtWidgets.QPushButton()
        self.studentPage.setFixedSize(410, 60)
        self.studentPage.setText("Student")
        self.studentPage.setCursor(QCursor(Qt.PointingHandCursor))
        self.studentPage.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.studentPage.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.studentPage)

        self.InstructorPage = QtWidgets.QPushButton()
        self.InstructorPage.setFixedSize(410, 60)
        self.InstructorPage.setCursor(QCursor(Qt.PointingHandCursor))
        self.InstructorPage.setText("Instructor")
        self.InstructorPage.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.InstructorPage.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.InstructorPage)

        self.RegistrarsPage = QtWidgets.QPushButton()
        self.RegistrarsPage.setFixedSize(410, 60)
        self.RegistrarsPage.setCursor(QCursor(Qt.PointingHandCursor))
        self.RegistrarsPage.setText("Registrars")
        self.RegistrarsPage.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.RegistrarsPage.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.RegistrarsPage)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.stBTNS = QWidget()
        self.stBTNSL = QHBoxLayout()

        self.newInstructorBTN = QtWidgets.QPushButton()
        self.newInstructorBTN.setText("New Instructor")
        self.newInstructorBTN.setFont(QFont("Century Gothic", 26))
        self.newInstructorBTN.setFixedSize(380, 90)
        self.newInstructorBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.newInstructorBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.stBTNSL.addWidget(self.newInstructorBTN)

        self.existingInstructorBTN = QtWidgets.QPushButton()
        self.existingInstructorBTN.setText("Existing Instructor")
        self.existingInstructorBTN.setFont(QFont("Century Gothic", 26))
        self.existingInstructorBTN.setFixedSize(380, 90)
        self.existingInstructorBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.existingInstructorBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.stBTNSL.addWidget(self.existingInstructorBTN)

        self.stBTNS.setLayout(self.stBTNSL)
        self.mainL.addWidget(self.stBTNS)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        self.existingInstructorBTN.clicked.connect(self.startup_page_instructor)
        self.newInstructorBTN.clicked.connect(self.instructorDetails)
        self.RegistrarsPage.clicked.connect(self.StartupRegistrars)
        self.studentPage.clicked.connect(self.StartupStudent)
        # self.startup_page()

    def StartupRegistrars(self):
        global loginState
        loginState = "Registrar"
        # Registrars Window

        # setting background colour for the page
        self.setStyleSheet("background-color:#031926;")
        self.mainW = QWidget()
        self.mainL = QVBoxLayout()

        self.navbarW = QWidget()
        self.navbarL = QHBoxLayout()
        self.navbarW.setFixedHeight(80)
        self.navbarW.setFixedWidth(1240)
        self.navbarW.setStyleSheet("border-bottom: 1px solid white;")

        self.studentPage = QtWidgets.QPushButton()
        self.studentPage.setFixedSize(410, 60)
        self.studentPage.setText("Student")
        self.studentPage.setCursor(QCursor(Qt.PointingHandCursor))
        self.studentPage.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.studentPage.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.studentPage)

        self.InstructorPage = QtWidgets.QPushButton()
        self.InstructorPage.setFixedSize(410, 60)
        self.InstructorPage.setCursor(QCursor(Qt.PointingHandCursor))
        self.InstructorPage.setText("Instructor")
        self.InstructorPage.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.InstructorPage.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.InstructorPage)

        self.RegistrarsPage = QtWidgets.QPushButton()
        self.RegistrarsPage.setFixedSize(410, 60)
        self.RegistrarsPage.setCursor(QCursor(Qt.PointingHandCursor))
        self.RegistrarsPage.setText("Registrars")
        self.RegistrarsPage.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.RegistrarsPage.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.RegistrarsPage)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.stBTNS = QWidget()
        self.stBTNSL = QHBoxLayout()

        self.loginbtn = QtWidgets.QPushButton()
        self.loginbtn.setText("Log in")
        self.loginbtn.setFont(QFont("Century Gothic", 26))
        self.loginbtn.setFixedSize(380, 90)
        self.loginbtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.loginbtn.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.stBTNSL.addWidget(self.loginbtn)

        self.stBTNS.setLayout(self.stBTNSL)
        self.mainL.addWidget(self.stBTNS)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.setCentralWidget(self.mainW)

        self.studentPage.clicked.connect(self.StartupStudent)
        self.InstructorPage.clicked.connect(self.StartupInstructor)
        self.loginbtn.clicked.connect(self.startup_page_registrar)
        # self.startup_page()

    def addInsApplicant(self):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """INSERT INTO applicants(first, last, email, resume, user_type) VALUES (?, ?, ?, ?, ?)""",
            (
                str(self.firstnameBOX.text()),
                str(self.lastnameBOX.text()),
                str(self.emailBOX.text()),
                str(self.ResumeBOX.text()),
                "instructor",
            ),
        )
        conn.commit()
        conn.close()
        self.startup_page_instructor()

    def instructorDetails(self):
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

        self.secondNameTXT = QtWidgets.QLabel()
        self.secondNameTXT.setText("Middle name :")
        self.secondNameTXT.setStyleSheet("color:white;")
        self.secondNameTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.secondNameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.secondnameBOX = QtWidgets.QLineEdit()
        self.secondnameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.secondnameBOX.setFont(QFont("Century Gothic", 16))
        self.secondnameBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.secondnameBOX)

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

        self.QualificationsTXT = QtWidgets.QLabel()
        self.QualificationsTXT.setText("Qualifications :")
        self.QualificationsTXT.setStyleSheet("color:white;")
        self.QualificationsTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.QualificationsTXT)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.QualificationsBOX = QtWidgets.QLineEdit()
        self.QualificationsBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.QualificationsBOX.setFont(QFont("Century Gothic", 16))
        self.QualificationsBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.QualificationsBOX)

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

        self.numcoursesTXT = QtWidgets.QLabel()
        self.numcoursesTXT.setText("Birth date :")
        self.numcoursesTXT.setStyleSheet("color:white;")
        self.numcoursesTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL.addWidget(self.numcoursesTXT)

        self.space = QWidget()
        self.space.setFixedHeight(12)
        self.boxesL.addWidget(self.space)

        self.numcoursesBOX = QtWidgets.QLineEdit()
        self.numcoursesBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.numcoursesBOX.setFont(QFont("Century Gothic", 16))
        self.numcoursesBOX.setFixedSize(300, 30)
        self.boxesL.addWidget(self.numcoursesBOX)

        self.HomeAdressTXT = QtWidgets.QLabel()
        self.HomeAdressTXT.setText("Permanent home address :")
        self.HomeAdressTXT.setStyleSheet("color:white;")
        self.HomeAdressTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.HomeAdressTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL2.addWidget(self.space)

        self.HomeAdressBOX = QtWidgets.QLineEdit()
        self.HomeAdressBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.HomeAdressBOX.setFont(QFont("Century Gothic", 16))
        self.HomeAdressBOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.HomeAdressBOX)

        self.CityTXT = QtWidgets.QLabel()
        self.CityTXT.setText("City :")
        self.CityTXT.setStyleSheet("color:white;")
        self.CityTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.CityTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL2.addWidget(self.space)

        self.CityBOX = QtWidgets.QLineEdit()
        self.CityBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.CityBOX.setFont(QFont("Century Gothic", 16))
        self.CityBOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.CityBOX)

        self.StateTXT = QtWidgets.QLabel()
        self.StateTXT.setText("State :")
        self.StateTXT.setStyleSheet("color:white;")
        self.StateTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.StateTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL2.addWidget(self.space)

        self.StateBOX = QtWidgets.QLineEdit()
        self.StateBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.StateBOX.setFont(QFont("Century Gothic", 16))
        self.StateBOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.StateBOX)

        self.ZipcodeTXT = QtWidgets.QLabel()
        self.ZipcodeTXT.setText("Zip-code :")
        self.ZipcodeTXT.setStyleSheet("color:white;")
        self.ZipcodeTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.ZipcodeTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL2.addWidget(self.space)

        self.ZipcodeBOX = QtWidgets.QLineEdit()
        self.ZipcodeBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.ZipcodeBOX.setFont(QFont("Century Gothic", 16))
        self.ZipcodeBOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.ZipcodeBOX)

        self.CurrentMATXT = QtWidgets.QLabel()
        self.CurrentMATXT.setText("Current mailing address :")
        self.CurrentMATXT.setStyleSheet("color:white;")
        self.CurrentMATXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.CurrentMATXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL2.addWidget(self.space)

        self.CurrentMABOX = QtWidgets.QLineEdit()
        self.CurrentMABOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.CurrentMABOX.setFont(QFont("Century Gothic", 16))
        self.CurrentMABOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.CurrentMABOX)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL2.addWidget(self.space)

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

        self.CoverLetterTXT = QtWidgets.QLabel()
        self.CoverLetterTXT.setText("Cover letter :")
        self.CoverLetterTXT.setStyleSheet("color:white;")
        self.CoverLetterTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.CoverLetterTXT)

        self.space = QWidget()
        self.space.setFixedHeight(18)
        self.boxesL2.addWidget(self.space)

        self.CoverLetterBOX = QtWidgets.QLineEdit()
        self.CoverLetterBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.CoverLetterBOX.setFont(QFont("Century Gothic", 16))
        self.CoverLetterBOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.CoverLetterBOX)

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

        self.saveBTN.clicked.connect(self.addInsApplicant)
        # run startup_page_instructor in the addInsApplicant
        # self.saveBTN.clicked.connect(self.startup_page_instructor)
        self.backBTN.clicked.connect(self.StartupInstructor)

    def studentDetails(self):
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
        self.GPATXT.setText("What is your GPA :")
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

        self.HomeAdressTXT = QtWidgets.QLabel()
        self.HomeAdressTXT.setText("Permanent home address :")
        self.HomeAdressTXT.setStyleSheet("color:white;")
        self.HomeAdressTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.HomeAdressTXT)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL2.addWidget(self.space)

        self.HomeAdressBOX = QtWidgets.QLineEdit()
        self.HomeAdressBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.HomeAdressBOX.setFont(QFont("Century Gothic", 16))
        self.HomeAdressBOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.HomeAdressBOX)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL2.addWidget(self.space)

        self.CityTXT = QtWidgets.QLabel()
        self.CityTXT.setText("City :")
        self.CityTXT.setStyleSheet("color:white;")
        self.CityTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.CityTXT)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL2.addWidget(self.space)

        self.CityBOX = QtWidgets.QLineEdit()
        self.CityBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.CityBOX.setFont(QFont("Century Gothic", 16))
        self.CityBOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.CityBOX)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL2.addWidget(self.space)

        self.StateTXT = QtWidgets.QLabel()
        self.StateTXT.setText("State :")
        self.StateTXT.setStyleSheet("color:white;")
        self.StateTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.StateTXT)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL2.addWidget(self.space)

        self.StateBOX = QtWidgets.QLineEdit()
        self.StateBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.StateBOX.setFont(QFont("Century Gothic", 16))
        self.StateBOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.StateBOX)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL2.addWidget(self.space)

        self.ZipcodeTXT = QtWidgets.QLabel()
        self.ZipcodeTXT.setText("Zip-code :")
        self.ZipcodeTXT.setStyleSheet("color:white;")
        self.ZipcodeTXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.ZipcodeTXT)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL2.addWidget(self.space)

        self.ZipcodeBOX = QtWidgets.QLineEdit()
        self.ZipcodeBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.ZipcodeBOX.setFont(QFont("Century Gothic", 16))
        self.ZipcodeBOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.ZipcodeBOX)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL2.addWidget(self.space)

        self.CurrentMATXT = QtWidgets.QLabel()
        self.CurrentMATXT.setText("Current mailing address :")
        self.CurrentMATXT.setStyleSheet("color:white;")
        self.CurrentMATXT.setFont(QFont("Century Gothic", 16))
        self.boxesL2.addWidget(self.CurrentMATXT)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL2.addWidget(self.space)

        self.CurrentMABOX = QtWidgets.QLineEdit()
        self.CurrentMABOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.CurrentMABOX.setFont(QFont("Century Gothic", 16))
        self.CurrentMABOX.setFixedSize(300, 30)
        self.boxesL2.addWidget(self.CurrentMABOX)

        self.space = QWidget()
        self.space.setFixedHeight(20)
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

        self.saveBTN.clicked.connect(self.startup_page_student)
        self.backBTN.clicked.connect(self.StartupStudent)

    def startup_page_student(self):
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
        self.highestRatedClassesTXT.setText("Highest rated classes")
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
        self.lowestRatedClassesTXT.setText("Lowest rated classes")
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
        self.highestGPATXT.setText("Highest GPA Students")
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

        self.signUpBTN = QtWidgets.QPushButton()
        self.signUpBTN.setText("Sign Up")
        self.signUpBTN.setFont(QFont("Century Gothic", 20))
        self.signUpBTN.setFixedSize(180, 60)
        self.signUpBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.signUpBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.logSignL.addWidget(self.space)
        self.logSignL.addWidget(self.signUpBTN)

        # start of adding the back button

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.logSignL.addWidget(self.space)
        self.logSignL.addWidget(self.backToStartupBTN)

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
        self.backToStartupBTN.clicked.connect(self.StartupStudent)
        self.signUpBTN.clicked.connect(self.signup_page)

    def startup_page_instructor(self):
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
        self.highestRatedClassesTXT.setText("Highest rated classes")
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
        self.lowestRatedClassesTXT.setText("Lowest rated classes")
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
        self.highestGPATXT.setText("Highest GPA Students")
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

        self.signUpBTN = QtWidgets.QPushButton()
        self.signUpBTN.setText("Sign Up")
        self.signUpBTN.setFont(QFont("Century Gothic", 20))
        self.signUpBTN.setFixedSize(180, 60)
        self.signUpBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.signUpBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.logSignL.addWidget(self.space)
        self.logSignL.addWidget(self.signUpBTN)

        # start of adding the back button

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.logSignL.addWidget(self.space)
        self.logSignL.addWidget(self.backToStartupBTN)

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
        self.backToStartupBTN.clicked.connect(self.StartupStudent)
        self.signUpBTN.clicked.connect(self.signup_page)

    def startup_page_registrar(self):
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
        self.highestRatedClassesTXT.setText("Highest rated classes")
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
        self.lowestRatedClassesTXT.setText("Lowest rated classes")
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
        self.highestGPATXT.setText("Highest GPA Students")
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

        self.signUpBTN = QtWidgets.QPushButton()
        self.signUpBTN.setText("Sign Up")
        self.signUpBTN.setFont(QFont("Century Gothic", 20))
        self.signUpBTN.setFixedSize(180, 60)
        self.signUpBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.signUpBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.logSignL.addWidget(self.space)
        self.logSignL.addWidget(self.signUpBTN)

        # start of adding the back button

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.logSignL.addWidget(self.space)
        self.logSignL.addWidget(self.backToStartupBTN)

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
        self.backToStartupBTN.clicked.connect(self.StartupStudent)
        self.signUpBTN.clicked.connect(self.signup_page)

    def compliant_page(self):
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
        self.complaintTXT.setText("Compliant :")
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

        self.back.clicked.connect(self.mainpage_home)

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

        self.nameTXT = QtWidgets.QLabel()
        self.nameTXT.setText("Name :")
        self.nameTXT.setStyleSheet("color:white;")
        self.nameTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.nameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(30)
        self.boxesL.addWidget(self.space)

        self.nameBOX = QtWidgets.QLineEdit()
        self.nameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.nameBOX.setFont(QFont("Century Gothic", 20))
        self.nameBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.nameBOX)

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
        self.nameTXT.setText("Name :")
        self.nameTXT.setStyleSheet("color:white;")
        self.nameTXT.setFont(QFont("Century Gothic", 20))
        self.boxesL.addWidget(self.nameTXT)

        self.space = QWidget()
        self.space.setFixedHeight(20)
        self.boxesL.addWidget(self.space)

        self.nameBOX = QtWidgets.QLineEdit()
        self.nameBOX.setStyleSheet(
            "color:black;background-color:white;padding-left:20;border-radius:10px;"
        )
        self.nameBOX.setFont(QFont("Century Gothic", 20))
        self.nameBOX.setFixedSize(600, 60)
        self.boxesL.addWidget(self.nameBOX)

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

        self.forgotPass = QtWidgets.QPushButton()
        self.forgotPass.setCursor(QCursor(Qt.PointingHandCursor))
        self.forgotPass.setText("Forgotten your password ?")
        self.forgotPass.setFont(QFont("Century Gothic", 16))
        self.forgotPass.setStyleSheet("background-color: transparent;color:white;")

        self.boxesL.addWidget(self.forgotPass)

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
        print(f"self.nameBOX = {self.nameBOX.text()}")
        self.backToMainBTN.clicked.connect(self.StartupStudent)
        self.signUpBTN.clicked.connect(self.signup_page)
        self.loginFBTN.clicked.connect(self.login)

    def mainpage_home(self):
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

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToStartupBTN)

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
        self.home.clicked.connect(self.mainpage_home)
        self.account.clicked.connect(self.mainpage_account)
        self.backToStartupBTN.clicked.connect(self.StartupStudent)
        self.help.clicked.connect(self.mainpage_help)
        self.ComplaintBTN.clicked.connect(self.compliant_page)
        self.classes.clicked.connect(self.mainpage_classes)

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

        self.accountType = QtWidgets.QLabel()
        self.accountType.setText(acc_type)
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

        self.home.clicked.connect(self.mainpage_home)
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

        self.BTNSW = QWidget()
        self.BTNSL = QHBoxLayout()

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToStartupBTN)

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

        self.home.clicked.connect(self.mainpage_home)
        self.account.clicked.connect(self.mainpage_account)
        self.help.clicked.connect(self.mainpage_help)
        self.classes.clicked.connect(self.mainpage_classes)
        self.backToStartupBTN.clicked.connect(self.StartupStudent)

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

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToStartupBTN)

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

        global classes
        self.classesW = QWidget()
        self.classesL = QVBoxLayout()

        for i in classes:
            self.StudentClassW = QtWidgets.QWidget()
            self.StudentClassW.setStyleSheet(
                "background-color:white;border-radius:15px;"
            )
            self.StudentClassL = QHBoxLayout()

            self.className = QtWidgets.QLabel()
            self.className.setFixedWidth(180)
            self.className.setText(f"Name:\n\n{i[0]}")
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

        self.home.clicked.connect(self.mainpage_home)
        self.account.clicked.connect(self.mainpage_account)
        self.help.clicked.connect(self.mainpage_help)
        self.classes.clicked.connect(self.mainpage_classes)
        self.backToStartupBTN.clicked.connect(self.StartupStudent)

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

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToStartupBTN)

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
        self.backToStartupBTN.clicked.connect(self.StartupStudent)
        self.help.clicked.connect(self.mainpage_help_instructor)
        self.ComplaintBTN.clicked.connect(self.compliant_page)
        self.classes.clicked.connect(self.mainpage_classes_instructor)

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
        self.accountType.setText(acc_type)
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

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToStartupBTN)

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
        self.help.clicked.connect(self.mainpage_help_instructor)
        self.classes.clicked.connect(self.mainpage_classes_instructor)
        self.backToStartupBTN.clicked.connect(self.StartupStudent)

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

        self.BTNSW = QWidget()
        self.BTNSL = QHBoxLayout()

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToStartupBTN)

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
        self.backToStartupBTN.clicked.connect(self.StartupStudent)

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

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToStartupBTN)

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
        self.home.clicked.connect(self.mainpage_home_registrar)
        self.applicationsBTN.clicked.connect(self.applications)  # Aiman 11/6
        self.account.clicked.connect(self.mainpage_account_registrar)
        self.backToStartupBTN.clicked.connect(self.StartupStudent)
        self.help.clicked.connect(self.mainpage_help_registrar)
        self.ComplaintBTN.clicked.connect(self.compliant_page)
        self.classes.clicked.connect(self.mainpage_classes_registrar)

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
        self.accountType.setText(acc_type)
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

        self.BTNSW = QWidget()
        self.BTNSL = QHBoxLayout()

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToStartupBTN)

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

        self.home.clicked.connect(self.mainpage_home_registrar)
        self.account.clicked.connect(self.mainpage_account_registrar)
        self.help.clicked.connect(self.mainpage_help_registrar)
        self.classes.clicked.connect(self.mainpage_classes_registrar)
        self.backToStartupBTN.clicked.connect(self.StartupStudent)

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

        self.backToStartupBTN = QtWidgets.QPushButton()
        self.backToStartupBTN.setText("Back")
        self.backToStartupBTN.setFont(QFont("Century Gothic", 20))
        self.backToStartupBTN.setFixedSize(180, 60)
        self.backToStartupBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToStartupBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToStartupBTN)

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

        global instructors
        for i in instructors:
            self.instructor.addItem(str(f"  {i}"))

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

        self.scheduleTXT = QtWidgets.QLabel()
        self.scheduleTXT.setText("Schedule :")
        self.scheduleTXT.setStyleSheet("color:white;padding-bottom:10px;")
        self.scheduleTXT.setFont(QFont("Century Gothic", 20))

        self.mondayW = QWidget()
        self.mondayL = QHBoxLayout()

        self.mondayTXT = QtWidgets.QLabel()
        self.mondayTXT.setText("Monday :")
        self.mondayTXT.setStyleSheet("color:white;padding-bottom:10px;")
        self.mondayTXT.setFont(QFont("Century Gothic", 18))

        self.mondayHRS_min = QtWidgets.QComboBox()
        self.mondayHRS_min.setStyleSheet(comboBox_stylesheet)
        self.mondayHRS_min.setFont(QFont("Century Gothic", 16))
        self.mondayHRS_min.setFixedSize(60, 45)
        self.mondayHRS_min.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(24):
            self.mondayHRS_min.addItem(str(i + 1))

        self.mondayMIN_min = QtWidgets.QComboBox()
        self.mondayMIN_min.setStyleSheet(comboBox_stylesheet)
        self.mondayMIN_min.setFont(QFont("Century Gothic", 16))
        self.mondayMIN_min.setFixedSize(60, 45)
        self.mondayMIN_min.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(59):
            self.mondayMIN_min.addItem(str(i + 1))

        self.mondayHRS_max = QtWidgets.QComboBox()
        self.mondayHRS_max.setStyleSheet(comboBox_stylesheet)
        self.mondayHRS_max.setFont(QFont("Century Gothic", 16))
        self.mondayHRS_max.setFixedSize(60, 45)
        self.mondayHRS_max.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(24):
            self.mondayHRS_max.addItem(str(i + 1))

        self.mondayMIN_max = QtWidgets.QComboBox()
        self.mondayMIN_max.setStyleSheet(comboBox_stylesheet)
        self.mondayMIN_max.setFont(QFont("Century Gothic", 16))
        self.mondayMIN_max.setFixedSize(60, 45)
        self.mondayMIN_max.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(59):
            self.mondayMIN_max.addItem(str(i + 1))

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.mondayL.addWidget(self.mondayTXT)
        self.mondayL.addWidget(self.mondayHRS_min)
        self.mondayL.addWidget(self.mondayMIN_min)
        self.mondayL.addWidget(self.space)
        self.mondayL.addWidget(self.mondayHRS_max)
        self.mondayL.addWidget(self.mondayMIN_max)
        self.mondayW.setLayout(self.mondayL)

        self.tuesdayW = QWidget()
        self.tuesdayL = QHBoxLayout()

        self.tuesdayTXT = QtWidgets.QLabel()
        self.tuesdayTXT.setText("Tuesday :")
        self.tuesdayTXT.setStyleSheet("color:white;padding-bottom:10px;")
        self.tuesdayTXT.setFont(QFont("Century Gothic", 18))

        self.tuesdayHRS_min = QtWidgets.QComboBox()
        self.tuesdayHRS_min.setStyleSheet(comboBox_stylesheet)
        self.tuesdayHRS_min.setFont(QFont("Century Gothic", 16))
        self.tuesdayHRS_min.setFixedSize(60, 45)
        self.tuesdayHRS_min.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(24):
            self.tuesdayHRS_min.addItem(str(i + 1))

        self.tuesdayMIN_min = QtWidgets.QComboBox()
        self.tuesdayMIN_min.setStyleSheet(comboBox_stylesheet)
        self.tuesdayMIN_min.setFont(QFont("Century Gothic", 16))
        self.tuesdayMIN_min.setFixedSize(60, 45)
        self.tuesdayMIN_min.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(59):
            self.tuesdayMIN_min.addItem(str(i + 1))

        self.tuesdayHRS_max = QtWidgets.QComboBox()
        self.tuesdayHRS_max.setStyleSheet(comboBox_stylesheet)
        self.tuesdayHRS_max.setFont(QFont("Century Gothic", 16))
        self.tuesdayHRS_max.setFixedSize(60, 45)
        self.tuesdayHRS_max.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(24):
            self.tuesdayHRS_max.addItem(str(i + 1))

        self.tuesdayMIN_max = QtWidgets.QComboBox()
        self.tuesdayMIN_max.setStyleSheet(comboBox_stylesheet)
        self.tuesdayMIN_max.setFont(QFont("Century Gothic", 16))
        self.tuesdayMIN_max.setFixedSize(60, 45)
        self.tuesdayMIN_max.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(59):
            self.tuesdayMIN_max.addItem(str(i + 1))

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.tuesdayL.addWidget(self.tuesdayTXT)
        self.tuesdayL.addWidget(self.tuesdayHRS_min)
        self.tuesdayL.addWidget(self.tuesdayMIN_min)
        self.tuesdayL.addWidget(self.space)
        self.tuesdayL.addWidget(self.tuesdayHRS_max)
        self.tuesdayL.addWidget(self.tuesdayMIN_max)
        self.tuesdayW.setLayout(self.tuesdayL)

        self.wednesdayW = QWidget()
        self.wednesdayL = QHBoxLayout()

        self.wednesdayTXT = QtWidgets.QLabel()
        self.wednesdayTXT.setText("wednesday :")
        self.wednesdayTXT.setStyleSheet("color:white;padding-bottom:10px;")
        self.wednesdayTXT.setFont(QFont("Century Gothic", 18))

        self.wednesdayHRS_min = QtWidgets.QComboBox()
        self.wednesdayHRS_min.setStyleSheet(comboBox_stylesheet)
        self.wednesdayHRS_min.setFont(QFont("Century Gothic", 16))
        self.wednesdayHRS_min.setFixedSize(60, 45)
        self.wednesdayHRS_min.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(24):
            self.wednesdayHRS_min.addItem(str(i + 1))

        self.wednesdayMIN_min = QtWidgets.QComboBox()
        self.wednesdayMIN_min.setStyleSheet(comboBox_stylesheet)
        self.wednesdayMIN_min.setFont(QFont("Century Gothic", 16))
        self.wednesdayMIN_min.setFixedSize(60, 45)
        self.wednesdayMIN_min.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(59):
            self.wednesdayMIN_min.addItem(str(i + 1))

        self.wednesdayHRS_max = QtWidgets.QComboBox()
        self.wednesdayHRS_max.setStyleSheet(comboBox_stylesheet)
        self.wednesdayHRS_max.setFont(QFont("Century Gothic", 16))
        self.wednesdayHRS_max.setFixedSize(60, 45)
        self.wednesdayHRS_max.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(24):
            self.wednesdayHRS_max.addItem(str(i + 1))

        self.wednesdayMIN_max = QtWidgets.QComboBox()
        self.wednesdayMIN_max.setStyleSheet(comboBox_stylesheet)
        self.wednesdayMIN_max.setFont(QFont("Century Gothic", 16))
        self.wednesdayMIN_max.setFixedSize(60, 45)
        self.wednesdayMIN_max.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(59):
            self.wednesdayMIN_max.addItem(str(i + 1))

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.wednesdayL.addWidget(self.wednesdayTXT)
        self.wednesdayL.addWidget(self.wednesdayHRS_min)
        self.wednesdayL.addWidget(self.wednesdayMIN_min)
        self.wednesdayL.addWidget(self.space)
        self.wednesdayL.addWidget(self.wednesdayHRS_max)
        self.wednesdayL.addWidget(self.wednesdayMIN_max)
        self.wednesdayW.setLayout(self.wednesdayL)

        self.thursdayW = QWidget()
        self.thursdayL = QHBoxLayout()

        self.thursdayTXT = QtWidgets.QLabel()
        self.thursdayTXT.setText("Thursday :")
        self.thursdayTXT.setStyleSheet("color:white;padding-bottom:10px;")
        self.thursdayTXT.setFont(QFont("Century Gothic", 18))

        self.thursdayHRS_min = QtWidgets.QComboBox()
        self.thursdayHRS_min.setStyleSheet(comboBox_stylesheet)
        self.thursdayHRS_min.setFont(QFont("Century Gothic", 16))
        self.thursdayHRS_min.setFixedSize(60, 45)
        self.thursdayHRS_min.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(24):
            self.thursdayHRS_min.addItem(str(i + 1))

        self.thursdayMIN_min = QtWidgets.QComboBox()
        self.thursdayMIN_min.setStyleSheet(comboBox_stylesheet)
        self.thursdayMIN_min.setFont(QFont("Century Gothic", 16))
        self.thursdayMIN_min.setFixedSize(60, 45)
        self.thursdayMIN_min.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(59):
            self.thursdayMIN_min.addItem(str(i + 1))

        self.thursdayHRS_max = QtWidgets.QComboBox()
        self.thursdayHRS_max.setStyleSheet(comboBox_stylesheet)
        self.thursdayHRS_max.setFont(QFont("Century Gothic", 16))
        self.thursdayHRS_max.setFixedSize(60, 45)
        self.thursdayHRS_max.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(24):
            self.thursdayHRS_max.addItem(str(i + 1))

        self.thursdayMIN_max = QtWidgets.QComboBox()
        self.thursdayMIN_max.setStyleSheet(comboBox_stylesheet)
        self.thursdayMIN_max.setFont(QFont("Century Gothic", 16))
        self.thursdayMIN_max.setFixedSize(60, 45)
        self.thursdayMIN_max.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(59):
            self.thursdayMIN_max.addItem(str(i + 1))

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.thursdayL.addWidget(self.thursdayTXT)
        self.thursdayL.addWidget(self.thursdayHRS_min)
        self.thursdayL.addWidget(self.thursdayMIN_min)
        self.thursdayL.addWidget(self.space)
        self.thursdayL.addWidget(self.thursdayHRS_max)
        self.thursdayL.addWidget(self.thursdayMIN_max)
        self.thursdayW.setLayout(self.thursdayL)

        self.fridayW = QWidget()
        self.fridayL = QHBoxLayout()

        self.fridayTXT = QtWidgets.QLabel()
        self.fridayTXT.setText("Friday :")
        self.fridayTXT.setStyleSheet("color:white;padding-bottom:10px;")
        self.fridayTXT.setFont(QFont("Century Gothic", 18))

        self.fridayHRS_min = QtWidgets.QComboBox()
        self.fridayHRS_min.setStyleSheet(comboBox_stylesheet)
        self.fridayHRS_min.setFont(QFont("Century Gothic", 16))
        self.fridayHRS_min.setFixedSize(60, 45)
        self.fridayHRS_min.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(24):
            self.fridayHRS_min.addItem(str(i + 1))

        self.fridayMIN_min = QtWidgets.QComboBox()
        self.fridayMIN_min.setStyleSheet(comboBox_stylesheet)
        self.fridayMIN_min.setFont(QFont("Century Gothic", 16))
        self.fridayMIN_min.setFixedSize(60, 45)
        self.fridayMIN_min.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(59):
            self.fridayMIN_min.addItem(str(i + 1))

        self.fridayHRS_max = QtWidgets.QComboBox()
        self.fridayHRS_max.setStyleSheet(comboBox_stylesheet)
        self.fridayHRS_max.setFont(QFont("Century Gothic", 16))
        self.fridayHRS_max.setFixedSize(60, 45)
        self.fridayHRS_max.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(24):
            self.fridayHRS_max.addItem(str(i + 1))

        self.fridayMIN_max = QtWidgets.QComboBox()
        self.fridayMIN_max.setStyleSheet(comboBox_stylesheet)
        self.fridayMIN_max.setFont(QFont("Century Gothic", 16))
        self.fridayMIN_max.setFixedSize(60, 45)
        self.fridayMIN_max.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(59):
            self.fridayMIN_max.addItem(str(i + 1))

        self.space = QWidget()
        self.space.setFixedWidth(50)

        self.fridayL.addWidget(self.fridayTXT)
        self.fridayL.addWidget(self.fridayHRS_min)
        self.fridayL.addWidget(self.fridayMIN_min)
        self.fridayL.addWidget(self.space)
        self.fridayL.addWidget(self.fridayHRS_max)
        self.fridayL.addWidget(self.fridayMIN_max)
        self.fridayW.setLayout(self.fridayL)

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
        self.main_contentL.addWidget(self.scheduleTXT)
        self.main_contentL.addWidget(self.mondayW)
        self.main_contentL.addWidget(self.tuesdayW)
        self.main_contentL.addWidget(self.wednesdayW)
        self.main_contentL.addWidget(self.thursdayW)
        self.main_contentL.addWidget(self.fridayW)
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
        self.backToStartupBTN.clicked.connect(self.StartupStudent)

        # Aiman 11/6

    def addClass(self, addBtn):
        # change this if statement to If the class is actually added or not
        if True:
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
        self.backToHomeBTN.setText("Back")
        self.backToHomeBTN.setFont(QFont("Century Gothic", 20))
        self.backToHomeBTN.setFixedSize(180, 60)
        self.backToHomeBTN.setCursor(QCursor(Qt.PointingHandCursor))
        self.backToHomeBTN.setStyleSheet(
            "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
            "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
        )
        self.BTNSL.addWidget(self.backToHomeBTN)

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
        try:
            global applications

            self.applicationsW = QWidget()
            self.applicationsL = QVBoxLayout()

            for i in applications:
                self.StudentClassW = QtWidgets.QWidget()
                self.StudentClassW.setStyleSheet(
                    "background-color:white;border-radius:15px;"
                )
                self.StudentClassL = QHBoxLayout()

                self.firstName = QtWidgets.QLabel()
                self.firstName.setFixedWidth(180)
                self.firstName.setText(f"First name:\n\n{i[0]}")
                self.firstName.setFont(QFont("Century Gothic", 10))

                self.secondName = QtWidgets.QLabel()
                self.secondName.setText(f"Second name:\n\n{i[1]}")
                self.secondName.setFont(QFont("Century Gothic", 10))

                self.email = QtWidgets.QLabel()
                self.email.setText(f"E-mail:\n\n{i[2]}")
                self.email.setFont(QFont("Century Gothic", 10))

                self.GPA = QtWidgets.QLabel()
                self.GPA.setText(f"GPA:\n\n{i[3]}")
                self.GPA.setFont(QFont("Century Gothic", 10))

                self.resume = QtWidgets.QLabel()
                self.resume.setText(f"Resume:\n\n{i[4]}")
                self.resume.setFont(QFont("Century Gothic", 10))

                self.userType = QtWidgets.QLabel()
                self.userType.setText(f"User type:\n\n{i[5]}")
                self.userType.setFont(QFont("Century Gothic", 10))

                self.approveBTN = QtWidgets.QPushButton()
                self.approveBTN.setText("Approve")
                self.approveBTN.setFont(QFont("Century Gothic", 8))
                self.approveBTN.setFixedSize(70, 40)
                self.approveBTN.setStyleSheet(
                    "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
                    "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
                )

                self.denyBTN = QtWidgets.QPushButton()
                self.denyBTN.setText("Deny")
                self.denyBTN.setFont(QFont("Century Gothic", 8))
                self.denyBTN.setFixedSize(70, 40)
                self.denyBTN.setStyleSheet(
                    "QPushButton{background-color:#076DF2;border-radius: 10px;color: white;}"
                    "QPushButton:pressed{background-color: #03469e;border-style: inset;}"
                )

                space = QWidget()
                space.setFixedWidth(20)

                self.StudentClassL.addWidget(self.firstName)
                self.StudentClassL.addWidget(self.secondName)
                self.StudentClassL.addWidget(self.email)
                self.StudentClassL.addWidget(self.GPA)
                self.StudentClassL.addWidget(self.resume)
                self.StudentClassL.addWidget(self.userType)
                self.StudentClassL.addWidget(space)
                self.StudentClassL.addWidget(self.approveBTN)
                self.StudentClassL.addWidget(self.denyBTN)

                self.StudentClassW.setLayout(self.StudentClassL)
                self.applicationsL.addWidget(self.StudentClassW)

            self.applicationsW.setLayout(self.applicationsL)
            self.main_contentL.addWidget(self.applicationsW)
        except Exception as e:
            print(e)

        # -------------------------end------------------------------

        self.mainL.addWidget(self.backToHomeBTN)
        self.mainW.setLayout(self.mainL)
        self.mainL.addWidget(self.main_contentW)

        # -------------End of Design-------------

        applicant = sqlite3.connect("gsz.db")
        df = display_db.pd.read_sql_query("SELECT * FROM applicants", applicant)
        df = df.drop(["num_courses_taken", "applicant_id"], axis=1)

        model = display_db.pandasModel(df)
        view = QTableView()
        view.setModel(model)
        view.resize(800, 600)
        view.show()

        # scroll settings
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connecting the main layout and widget
        self.mainW.setLayout(self.mainL)
        self.scroll.setWidget(self.mainW)
        self.setCentralWidget(self.scroll)

        # checking if any buttons is clicked

        self.backToHomeBTN.clicked.connect(self.mainpage_home)

        # Aiman 11/6 end

    def logout(self):
        name = ""
        email = ""
        acc_type = ""
        id = ""
        self.startup_page_student()  # Aiman last change

    def signup(self):
        global id
        global acc_type
        global name
        global email

        conn = sqlite3.connect("gsz.db")

        c = conn.cursor()

        c.execute(
            "INSERT INTO applicants(Name, Email, Password, 'User ID', 'User Type') VALUES (?, ?, ?, ?, ?)",
            (
                str(self.nameBOX.text()),
                str(self.emailBOX.text()),
                str(self.passwordBOX.text()),
                generate_random(),
                str(self.combo.currentText()),
            ),
        )

        conn.commit()
        conn.close()

        name = self.nameBOX.text()
        email = self.emailBOX.text()
        acc_type = self.combo.currentText()
        self.mainpage_home()

    def login(self):
        global name
        global id
        global email
        global acc_type

        print(f"self.nameBOX = {self.nameBOX.text()}")

        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE id=? AND password=?",
            (self.nameBOX.text(), self.passwordBOX.text()),
        )
        row = c.fetchone()
        if row != None:
            # checking if it is a first login
            if row[7] == 1:
                # pop up window for setting up a new password
                # new_password = get from gui
                # user.change_password(new_password)
                pass
            # create instance of user
            if row[6] == "student":
                user = Student(row[0])
                self.mainpage_home()
            elif row[6] == "instructor":
                user = Instructor(row[0])
                self.mainpage_home_instructor()
            else:
                user = Registrar(row[0])
                self.mainpage_home_registrar()
        conn.close()
        self.tipsTXT.setText(
            "\n\n\n\n\n          Invalid user\n   Sign in to create an \n            account"
        )
        # create an instance of a user according to acc_type
        # find the user in appropriate db using primary key


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
        user_type text NOT NULL
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
        course_id integer NOT NULL,
        description text NOT NULL,
        complaint_type text,
        FOREIGN KEY ('complainant_id') REFERENCES users (user_id),
        FOREIGN KEY ('complainee_id') REFERENCES users (user_id),
        FOREIGN KEY ('course_id') REFERENCES courses (course_id)
        )"""
)
conn.commit()
conn.close()

# Running the Gui with the run of application
app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec_()

# plan
# buttons always exist, but if you are in the right period, they will function as they should,
# if you are not, they won't function and give you warning messages (use schedule module)
# use schedule module to play with buttons
