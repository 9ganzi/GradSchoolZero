from clas import Class
import sqlite3
import datetime


class User:
    def __init__(self, first, last, email, primary_key):
        self.first = first
        self.last = last
        self.email = email
        self.primary_key = primary_key


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
    def __init__(self, first, last, email, primary_key, classes):
        super().__init__(first, last, email, primary_key)
        conn = sqlite3.connect("student.db")
        c = conn.cursor()
        # row = list(c.execute("SELECT * FROM students WHERE ID = ?", (primary_key,)))[0]
        # self.classes = row[]
        # self.course_shitory = row[]

    def is_time_conflict(self, start, end):
        result = False
        for cls in self.classes:
            if (not (start > cls[1])) and (not (end < cls[0])):
                result = True
        return result

    def is_eligible(self, start, end):
        if (len(self.classes) >= 4) or (self.is_time_conflict(start, end)):
            return False

    def enroll_class(self, start, end, cls_primary_key):
        if self.is_eligible(start, end):
            pass


class Instructor:
    pass


# # testing class time conflict
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


# # testing database
# import sqlite3

# conn = sqlite3.connect("class.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS classes (ID integer PRIMARY KEY, Name text NOT NULL, 'Class Start' text NOT NULL, 'Class End' text NOT NULL, 'Class Size' integer NOT NULL, 'Student Classes ID' integer, 'Instructor Classes ID' integer, FOREIGN KEY ('Student Classes ID') REFERENCES student_classes (ID), FOREIGN KEY ('Instructor Classes ID') REFERENCES instructor_classes (ID))"""
#     # might use blob for 'Class Start' and 'Class End'
# )
# c.execute(
#     """INSERT INTO classes(Name, 'Class Start', 'Class End', 'Class Size') VALUES (?, ?, ?, ?)""",
#     ("CSC 520", "09:00:00", "10:00:00", 50),
# )
# conn.commit()
# c.close()

# conn = sqlite3.connect("student.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS students (ID integer PRIMARY KEY, 'Student Classes ID' integer, GPA real NOT NULL, 'Course History ID', 'User ID' integer, FOREIGN KEY ('Student Classes ID') REFERENCES student_classes (ID), FOREIGN KEY ('Course History ID') REFERENCES course_history (ID), FOREIGN KEY ('User ID') REFERENCES users (ID))"""
#     # might use blob for 'Class Start' and 'Class End'
# )
# c.execute(
#     """INSERT INTO students(GPA) VALUES (?)""",
#     (50,),
# )
# conn.commit()
# c.close()

# conn = sqlite3.connect("student_class.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS student_classes (ID integer PRIMARY KEY, 'Student ID' integer, 'Class ID' integer, FOREIGN KEY ('Student ID') REFERENCES students (ID), FOREIGN KEY ('Class ID') REFERENCES classes (ID))"""
#     # might use blob for 'Class Start' and 'Class End'
# )
# c.execute(
#     """INSERT INTO student_classes('Student ID', 'Class ID') VALUES (?, ?)""",
#     (1, 1),
# )
# conn.commit()
# c.close()
