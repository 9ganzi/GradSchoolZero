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

    def course_set_up(self, name, time, instructor, size):
        conn = sqlite3.connect("course.db")
        c = conn.cursor()
        c.execute(
            """INSERT INTO courses(course_name, course_rating, course_time, instructor_id, course_size, enroll_count, course_gpa) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                name,
                None,
                time,
                instructor,
                size,
                0,
                None,
            ),
        )
        conn.commit()
        conn.close()


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

    def is_time_conflict(self, course_id):
        conn = sqlite3.connect("enrollment.db")
        # to get a list of values instead of a list of tuples
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        c.execute(
            "SELECT course_id FROM enrollments WHERE student_id=?", (self.student_id,)
        )
        courses = c.fetchall()
        courses = list(map(int, courses))
        conn = sqlite3.connect("course.db")
        c = conn.cursor()
        c.execute(
            "SELECT course_time FROM courses WHERE course_id in ({courses})".format(
                courses=",".join(["?"] * len(courses))
            ),
            courses,
        )
        schedule = c.fetchall()
        schedule = [x[0].split(",") for x in schedule]
        schedule = [
            x2.replace(" - ", " ").strip().split(" ") for x1 in schedule for x2 in x1
        ]
        c.execute("SELECT course_time FROM courses WHERE course_id = ?", (course_id,))
        new_course = c.fetchone()[0]
        new_course = new_course.split(",")
        new_course = [x.strip().replace(" - ", " ").split(" ") for x in new_course]
        for day in schedule:
            for new_day in new_course:
                if day[0] == new_day[0]:
                    if (not (day[1] > new_day[1])) and (not (day[2] < new_day[2])):
                        return True
        return False

    def is_too_many_courses(self):
        conn = sqlite3.connect("enrollment.db")
        c = conn.cursor()
        c.execute(
            "SELECT enrollment_id FROM enrollments WHERE student_id = ?",
            (self.student_id,),
        )
        num_courses = len(c.fetchall())
        conn.close()
        if num_courses >= 4:
            return True
        return False

    def took_and_not_failed(self, course_id):
        conn = sqlite3.connect("course_history.db")
        c = conn.cursor()
        c.execute(
            "SELECT grade FROM course_historys WHERE student_id=? AND course_id=?",
            (self.student_id, course_id),
        )
        grade = c.fetchone()
        if type(grade) == tuple:
            grade = grade[0]
        if (grade == None) or (grade.lower() == "f"):
            return False
        return True

    def is_eligible(self, course_id):
        return (
            (not self.is_time_conflict(course_id))
            and (not self.is_too_many_courses())
            and (not self.took_and_not_failed(course_id))
        )

    def apply_wait_list(self, course_id):
        conn = sqlite3.connect("waitlist.db")
        c = conn.cursor()
        c.execute(
            """INSERT INTO waitlists(student_id, course_id) VALUES (?, ?)""",
            (
                self.student_id,
                course_id,
            ),
        )
        conn.commit()
        conn.close()

    def enroll_course(self, course_id):
        if self.is_eligible(course_id):
            if Course(course_id).is_full():
                self.apply_wait_list(course_id)
            return 0
        # enroll course
        return 1


class Instructor(User):
    def __init__(self, instructor_id):
        conn = sqlite3.connect("instructor.db")
        c = conn.cursor()
        c.execute("SELECT * FROM instructors WHERE instructor_id = ?", (instructor_id,))
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
# c.execute(
#     """INSERT INTO users(first, last, id, password, email, user_type) VALUES (?, ?, ?, ?, ?, ?)""",
#     ("Jaehong", "Cho", "id", "password", "email@email.com", "registrar"),
# )
# c.execute(
#     """INSERT INTO users(first, last, id, password, email, user_type) VALUES (?, ?, ?, ?, ?, ?)""",
#     ("John", "Doe", "id", "password", "email@email.com", "student"),
# )
# c.execute(
#     """INSERT INTO users(first, last, id, password, email, user_type) VALUES (?, ?, ?, ?, ?, ?)""",
#     ("Jane", "Doe", "id", "password", "email@emgail.com", "instructor"),
# )
# c.execute("SELECT * FROM users ORDER BY user_id DESC LIMIT 1")
# user_id = c.fetchone()[0]
# # print(user_id)
# conn.commit()
# conn.close()

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
# # conn.close()

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
# conn.close()

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
#         None,
#         "Th 11:00 - 12:15, Fr 1:00 - 2:30",
#         1,
#         15,
#         0,
#         None,
#     ),
# )
# conn.commit()
# conn.close()

# enrollment.db
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
#         6,
#         None,
#     ),
# )
# conn.commit()
# conn.close()

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
#         5,
#         "F",
#     ),
# )
# conn.commit()
# conn.close()

# # waitlist.db
# conn = sqlite3.connect("waitlist.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS waitlists (
#         waitlist_id integer PRIMARY KEY,
#         student_id integer NOT NULL,
#         course_id integer NOT NULL,
#         FOREIGN KEY ('student_id') REFERENCES students (student_id),
#         FOREIGN KEY ('course_id') REFERENCES courses (course_id)
#         )"""
# )
# c.execute(
#     """INSERT INTO waitlists(student_id, course_id) VALUES (?, ?)""",
#     (
#         1,
#         1,
#     ),
# )
# conn.commit()
# conn.close()

# # testing set up courses
# conn = sqlite3.connect("user.db")
# c = conn.cursor()
# c.execute("SELECT * FROM users WHERE user_id=1")
# args = c.fetchone()
# registrar1 = Registrar(args[0])
# conn = sqlite3.connect("instructor.db")
# c = conn.cursor()
# c.execute("SELECT * FROM instructors WHERE instructor_id=1")
# args = c.fetchone()
# instructor1 = Instructor(args[0])
# registrar1.course_set_up("CSC 33500", "Tu 12:00 - 1:15, We 12:00 - 2:30", args[0], 25)


# conn = sqlite3.connect("student.db")
# c = conn.cursor()
# c.execute("SELECT * FROM students WHERE student_id=?", (1,))
# args = c.fetchone()
# student1 = Student(args[0])
# print(student1.apply_wait_list(3))
# print(student1.apply_wait_list(4))
# print(student1.apply_wait_list(5))
# print(student1.apply_wait_list(6))


# sql = """ UPDATE courses
#               SET enroll_count = ?
#               WHERE course_id = ?"""
# conn = sqlite3.connect("course.db")
# c = conn.cursor()
# c.execute(sql, (26, 3))
# c.execute(sql, (25, 4))
# c.execute(sql, (15, 5))
# c.execute(sql, (18, 6))
# conn.commit()
# conn.close()

conn = sqlite3.connect("user.db")
c = conn.cursor()
c.execute(
    "INSERT INTO users (first, last, id, password, email, user_type) VALUES (?, ?, ?, ?, ?, ?)",
    ("Michael", "Jackson", "id", "password", "email@email.com", "registrar"),
)

# c.execute(
#     """INSERT INTO users(first, last, id, password, email, user_type) VALUES (?, ?, ?, ?, ?, ?)""",
#     ("Jaehong", "Cho", "id", "password", "email@email.com", "registrar"),
# )

conn.commit()
conn.close()
