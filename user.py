# 1. add a button to set up classes(only work for registrar)
# 2. set up class(name, time, instructor, size)
# @ add the class to the db
# 3. make all students register between 2-4 courses
# @ no time conflict
# # look at 'currently enrolled classes' of the student
# @ student didn't take the class before
# # look at 'course history(+grade)'
# @ or took it before but failed
# # look at 'course history(+grade)'
# @ course limit not reached
# # look at 'course enrolled count'
# - if limit reached, wait-list
# # add to the class database(wait-list attribute)

from clas import Cls
import sqlite3
import datetime


class User:
    def __init__(self, first, last, email):
        self.first = first
        self.last = last
        self.email = email


class Registrar:
    def __init__(self, first, last, email):
        super().__init__(first, last, email)

    def set_up_classes(
        self, name, instructor, start, end, size
    ):  # convert start and end to datetime before using the function
        if start > end:
            return -1  # error message on gui
        conn = sqlite3.connect("class.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS classes (Name text, Time text, 'Instructor' text, 'Class Start' text, 'Class End' text, ' Class Size' integer)"""
            # might use blob for 'Class Start' and 'Class End'
        )


class Student:
    def __init__(self, first, last, email):
        super().__init__(first, last, email)
        self.classes = []
        self.course_shitory = []

    def is_time_conflict(self, start, end):
        result = False
        for cls in self.classes:
            if (not (start > cls[1])) and (not (end < cls[0])):
                result = True
        return result

    def is_eligible(self, start, end):
        if (len(self.classes) >= 4) or (self.is_time_conflict(start, end)):
            return False

    def enroll_class(self, start, end):
        if self.is_eligible(start, end):
            pass


class Instructor:
    pass


# # test
# def test(start, end, classes):
#     result = True
#     for cls in classes:
#         if (not (start > cls[1])) and (not (end < cls[0])):
#             result = False
#     return result


# classes = [
#     [datetime.time(1, 00, 00), datetime.time(2, 00, 00)],
#     [datetime.time(3, 00, 00), datetime.time(4, 00, 00)],
#     [datetime.time(5, 00, 00), datetime.time(6, 00, 00)],
#     [datetime.time(7, 00, 00), datetime.time(8, 00, 00)],
# ]

# a_start = datetime.time(4, 59, 00)
# a_end = datetime.time(5, 00, 00)
# b_start = datetime.time(5, 30, 00)
# b_end = datetime.time(5, 31, 00)
# c_start = datetime.time(5, 31, 00)
# c_end = datetime.time(9, 00, 00)
# d_start = datetime.time(1, 00, 00)
# d_end = datetime.time(9, 00, 00)

# p_start = datetime.time(6, 1, 00)
# p_end = datetime.time(6, 20, 00)


# print(test(a_start, a_end, classes))
# print(test(b_start, b_end, classes))
# print(test(c_start, c_end, classes))
# print(test(d_start, d_end, classes))
# print(test(p_start, p_end, classes))
