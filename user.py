from course import Course, sqlite3


class User:
    def __init__(self, user_id):
        conn = sqlite3.connect("user.db")
        c = conn.cursor()
        c.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,))
        user_info = c.fetchone()
        conn.close()
        self.user_id = user_info[0]
        self.first = user_info[1]
        self.last = user_info[2]
        self.id = user_info[3]
        self.password = user_info[4]
        self.email = user_info[5]
        self.user_type = user_info[6]


class Registrar(User):
    def __init__(self, user_id):
        super().__init__(user_id)

    def set_up_courses(self, name, instructor, start, end, size):
        pass


class Student(User):
    def __init__(self, student_id):
        conn = sqlite3.connect("student.db")
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        student_info = c.fetchone()
        conn.close()
        super().__init__(student_info[1])
        self.student_id = student_info[0]
        self.gpa = student_info[2]
        self.num_courses_taken = student_info[3]
        self.honor_count = student_info[4]
        self.warning_count = student_info[5]

    def is_time_conflict(self, start, end):
        result = False
        for cls in self.courses:
            if (not (start > cls[1])) and (not (end < cls[0])):
                result = True
        return result

    def is_eligible(self, start, end):
        if (len(self.courses) >= 4) or (self.is_time_conflict(start, end)):
            return False

    def enroll_cours(self, start, end, cls_primary_key):
        if self.is_eligible(start, end):
            pass


class Instructor(User):
    def __init__(self, instructor_id):
        conn = sqlite3.connect("instructor.db")
        c = conn.cursor()
        c.execute("SELECT * FROM instructors WHERE student_id = ?", (instructor_id,))
        instructor_info = c.fetchone()
        conn.close()
        super().__init__(instructor_info[1])
        self.instructor_id = instructor_info[0]
        self.warning_count = instructor_info[2]
        self.is_suspended = instructor_info[3]


# # testing course time conflict
# def test(start, end, courses):
#     result = True
#     for cls in courses:
#         if (not (start > cls[1])) and (not (end < cls[0])):
#             result = False
#     return result


# courses = [
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


# print(test(a_start, a_end, courses))
# print(test(b_start, b_end, courses))
# print(test(c_start, c_end, courses))
# print(test(d_start, d_end, courses))
# print(test(p_start, p_end, courses))


# # # testing database
# # applicant.db
# conn = sqlite3.connect("applicant.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS applicants(
#         applicant_id integer PRIMARY KEY,
#         first text NOT NULL,
#         last text NOT NULL,
#         email text NOT NULL,
#         gpa real,
#         num_courses_taken integer,
#         user_type text NOT NULL
#         )"""
# )
# # c.execute(
# #     """INSERT INTO applicants(first, last, email, gpa, num_courses_taken, user_type) VALUES (?, ?, ?, ?, ?, ?)""",
# #     ("John", "Doe", "email@email.com", 5, 3, "student"),
# # )
# c.execute(
#     """INSERT INTO applicants(first, last, email, gpa, num_courses_taken, user_type) VALUES (?, ?, ?, ?, ?, ?)""",
#     ("Jane", "Doe", "email@email.com", None, None, "instructor"),
# )
# c.execute("SELECT * FROM applicants ORDER BY applicant_id DESC LIMIT 1")
# # select the latest row, the row we just inserted
# applicant_row = c.fetchone()
# print(applicant_row)
# conn.commit()
# conn.close()

# # user.db
# conn = sqlite3.connect("user.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS users (
#         user_id integer PRIMARY KEY,
#         first text NOT NULL,
#         last text NOT NULL,
#         id text NOT NULL,
#         password text NOT NULL,
#         email text NOT NULL,
#         user_type text NOT NULL)
#         """
# )
# # c.execute(
# #     """INSERT INTO users(first, last, id, password, email, user_type) VALUES (?, ?, ?, ?, ?, ?)""",
# #     ("Jaehong", "Cho", "id", "password", "email@email.com", "registrar"),
# # )
# # c.execute(
# #     """INSERT INTO users(first, last, id, password, email, user_type) VALUES (?, ?, ?, ?, ?, ?)""",
# #     ("John", "Doe", "id", "password", "email@email.com", "student"),
# # )
# c.execute(
#     """INSERT INTO users(first, last, id, password, email, user_type) VALUES (?, ?, ?, ?, ?, ?)""",
#     ("Jane", "Doe", "id", "password", "email@emgail.com", "instructor"),
# )
# c.execute("SELECT * FROM users ORDER BY user_id DESC LIMIT 1")
# user_id = c.fetchone()[0]
# # print(user_id)
# conn.commit()
# c.close()

# # # student.db
# # conn = sqlite3.connect("student.db")
# # c = conn.cursor()
# # c.execute(
# #     """CREATE TABLE IF NOT EXISTS students (
# #         student_id integer PRIMARY KEY,
# #         user_id integer NOT NULL,
# #         gpa real NOT NULL,
# #         num_courses_taken integer NOT NULL,
# #         honor_count integer NOT NULL,
# #         warning_count integer NOT NULL,
# #         FOREIGN KEY ('user_id') REFERENCES users (user_id)
# #         )"""
# # )
# # c.execute(
# #     """INSERT INTO students(user_id, gpa, honor_count, warning_count, num_courses_taken) VALUES (?, ?, ?, ?, ?)""",
# #     (user_id, applicant_row[4], 0, 0, applicant_row[5]),
# # )
# # conn.commit()
# # c.close()

# # instructor.db
# conn = sqlite3.connect("instructor.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS instructors (
#         instructor_id integer PRIMARY KEY,
#         user_id integer NOT NULL,
#         warning_count integer NOT NULL,
#         is_suspended integer NOT NULL,
#         FOREIGN KEY ('user_id') REFERENCES users (user_id)
#         )"""
# )
# c.execute(
#     """INSERT INTO instructors(user_id, warning_count, is_suspended) VALUES (?, ?, ?)""",
#     (user_id, 0, 0),
# )
# conn.commit()
# c.close()

# # course.db
# conn = sqlite3.connect("course.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS courses (
#         course_id integer PRIMARY KEY,
#         course_name text NOT NULL,
#         course_rating real,
#         course_time text NOT NULL,
#         instructor_id integer NOT NULL,
#         course_size integer NOT NULL,
#         enroll_count integer,
#         course_gpa real,
#         FOREIGN KEY ('instructor_id') REFERENCES users (user_id)
#         )"""
# )
# c.execute(
#     """INSERT INTO courses(course_name, course_rating, course_time, instructor_id, course_size, enroll_count, course_gpa) VALUES (?, ?, ?, ?, ?, ?, ?)""",
#     (
#         "CSC 59866",
#         5.0,
#         "TuTh 11:00 - 12:15, Fr 12:00 - 2:30",
#         1,
#         30,
#         0,
#         None,
#     ),
# )
# conn.commit()
# c.close()

# # enrollment.db
# conn = sqlite3.connect("enrollment.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS enrollments (
#         enrollment_id integer PRIMARY KEY,
#         student_id integer NOT NULL,
#         course_id integer NOT NULL,
#         grade real,
#         FOREIGN KEY ('student_id') REFERENCES students (student_id),
#         FOREIGN KEY ('course_id') REFERENCES courses (course_id)
#         )"""
# )
# c.execute(
#     """INSERT INTO enrollments(student_id, course_id, grade) VALUES (?, ?, ?)""",
#     (
#         1,
#         1,
#         None,
#     ),
# )
# conn.commit()
# c.close()

# # course_history.db
# conn = sqlite3.connect("course_history.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS course_historys (
#         course_history_id integer PRIMARY KEY,
#         student_id integer NOT NULL,
#         course_id integer NOT NULL,
#         grade real,
#         FOREIGN KEY ('student_id') REFERENCES students (student_id),
#         FOREIGN KEY ('course_id') REFERENCES courses (course_id)
#         )"""
# )
# c.execute(
#     """INSERT INTO course_historys(student_id, course_id, grade) VALUES (?, ?, ?)""",
#     (
#         1,
#         1,
#         None,
#     ),
# )
# conn.commit()
# c.close()

# waitlist.db
conn = sqlite3.connect("waitlist.db")
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS waitlists (
        waitlist_id integer PRIMARY KEY,
        student_id integer NOT NULL,
        course_id integer NOT NULL,
        instructor_id integer NOT NULL,
        FOREIGN KEY ('student_id') REFERENCES students (student_id),
        FOREIGN KEY ('course_id') REFERENCES courses (course_id),
        FOREIGN KEY ('instructor_id') REFERENCES instructors (instructor_id)
        )"""
)
c.execute(
    """INSERT INTO waitlists(student_id, course_id, instructor_id) VALUES (?, ?, ?)""",
    (
        1,
        1,
        1,
    ),
)
conn.commit()
c.close()


# # testing set up courses
# conn = sqlite3.connect("user.db")
# c = conn.cursor()
# c.execute("SELECT * FROM users WHERE ID=1")
# args = c.fetchone()
# r = Registrar("first", "last", args[0])
# a_start = "04:59:00"
# a_end = "05:00:00"
# r.set_up_courses("csc 32200", "Wei", a_start, a_end, 30)
