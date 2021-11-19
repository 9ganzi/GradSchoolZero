import sqlite3
import sys
import csv
import user
import schedule
import time
from periods import Period
import datetime
import os
import random
import string
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
        self.setWindowTitle("Collage App")
        self.setFixedSize(1260, 800)
        self.startup_page()

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
        self.signUpBTN.clicked.connect(self.signup_page)

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
        self.backToMainBTN.clicked.connect(self.startup_page)
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
        self.backToMainBTN.clicked.connect(self.startup_page)
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
        self.account.setFixedSize(410, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(410, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(410, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.main_contentL.addWidget(self.logo)

        self.main_contentW.setLayout(self.main_contentL)

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
        self.account.setFixedSize(410, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(410, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(410, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

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
        self.account.setFixedSize(410, 60)
        self.account.setText("Account")
        self.account.setCursor(QCursor(Qt.PointingHandCursor))
        self.account.setStyleSheet(
            "color:white;background:transparent;padding-bottom:10;"
        )
        self.account.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.account)

        self.home = QtWidgets.QPushButton()
        self.home.setFixedSize(410, 60)
        self.home.setCursor(QCursor(Qt.PointingHandCursor))
        self.home.setText("Home")
        self.home.setStyleSheet("color:white;background:transparent;padding-bottom:10;")
        self.home.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.home)

        self.help = QtWidgets.QPushButton()
        self.help.setFixedSize(410, 60)
        self.help.setCursor(QCursor(Qt.PointingHandCursor))
        self.help.setText("Help")
        self.help.setStyleSheet(
            "color:#076DF2;background:transparent;padding-bottom:10;"
        )
        self.help.setFont(QFont("Century Gothic", 20))
        self.navbarL.addWidget(self.help)

        self.navbarW.setLayout(self.navbarL)
        self.mainL.addWidget(self.navbarW)

        self.main_contentW = QWidget()
        self.main_contentL = QHBoxLayout()
        self.main_contentL.setAlignment(Qt.AlignTop)

        self.logoW = QWidget()

        self.logo = QtWidgets.QLabel(self.logoW)
        self.logo.setPixmap(QPixmap("logo.png"))
        self.main_contentL.addWidget(self.logo)

        self.main_contentW.setLayout(self.main_contentL)

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

    def logout(self):
        name = ""
        email = ""
        acc_type = ""
        id = ""
        self.startup_page()

    def signup(self):
        global id
        global acc_type
        global name
        global email

        conn = sqlite3.connect("user.db")

        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS users (Name text, Email text, Password text, ID text, 'User Type' text)"""
        )

        c.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
            (
                str(self.nameBOX.text()),
                str(self.emailBOX.text()),
                str(self.passwordBOX.text()),
                self.create_id(),
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

        conn = sqlite3.connect("user.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS users (Name text, Email text, Password text, ID text, 'User Type' text)"""
        )
        c.execute(
            "SELECT * FROM users WHERE name=? AND password=?",
            (self.nameBOX.text(), self.passwordBOX.text()),
        )
        row = c.fetchone()
        if row != None:
            name = row[0]
            email = row[1]
            id = row[3]
            acc_type = row[4]
            self.mainpage_home()
        self.tipsTXT.setText(
            "\n\n\n\n\n          Invalid user\n   Sign in to create an \n            account"
        )

    def create_id(self):
        letters = string.ascii_uppercase
        return "".join(random.choice(letters) for i in range(10))


# Running the Gui with the run of application
app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec_()

# plan
# buttons always exist, but if you are in the right period, they will function as they should,
# if you are not, they won't function and give you warning messages (use schedule module)
# use schedule module to play with buttons
