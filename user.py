import string
import random
from course import Course, sqlite3
import smtplib, ssl


def generate_random():
    letters = string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(10))


class User:
    def __init__(self, user_id):
        conn = sqlite3.connect("gsz.db")
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
        self.first_login = user_info[7]

    def is_first_login(self):
        return self.first_login == 1

    def change_password(self, new_password):
        self.password = new_password
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "UPDATE users SET password = ? WHERE user_id = ?"
        c.execute(sql, (new_password, self.user_id))
        conn.commit()
        conn.close()


# fire an instructor ( can only be accessed by registrar on their page)
# input a specfic instructor_id, deletes instructor from database
def fire_instructor(instructor_id):
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    c.execute(
        "DELETE FROM instructors WHERE instructor_id = :instructor_id",
        {"instructor_id": instructor_id},
    )
    conn.commit()
    conn.close()


# drop student from program ( can only be accessed by registrar on their page)
# given student class, delete student from database
def terminate_student(student):
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    c.execute(
        "DELETE * FROM students WHERE student_id = :student_id",
        {"student_id": student.student_id},
    )
    conn.commit()
    conn.close()


# drop student from program ( can only be accessed by registrar on their page)
# given student_id, delete student from database
def terminate_student(student_id):
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    c.execute(
        "DELETE * FROM students WHERE student_id = :student_id",
        {"student_id": student_id},
    )
    conn.commit()
    conn.close()


# graduates a student by setting degree to master ( can only be accessed by registrar on their page)
# inputs a student class, alterativelty should we just delete student from database as well
def graduate_student(student):
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    c.execute(
        """UPDATE student SET degree = :degree
                            WHERE student_id = student_id""",
        {"student_id": student.student_id, "degree": "Masters"},
    )
    conn.commit()
    conn.close()

    # issue warning to student ( can only be accessed by registrar on their page)
    # given a student_id


def issue_warning_std(student_id):
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor()
    # get current warning_count
    c.execute(
        "SELECT warning_count From students where student_id = :student_id",
        {"student_id": student_id},
    )
    new_warning_count = (
        c.fetchone()[0] + 1
    )  # c.fetchone()[0] isolate variable from tuple
    # print(new_warning_count)
    # update student warning_count
    c.execute(
        """UPDATE students SET warning_count = :new_warning_count
                        WHERE student_id =:student_id""",
        {"student_id": student_id, "new_warning_count": new_warning_count},
    )
    conn.commit()
    conn.close()

    # issue warning to instructor ( can only be accessed by registrar on their page)
    # given a instructor_id


def issue_warning_instuctor(instructor_id):
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


class Registrar(User):
    def __init__(self, user_id):
        super().__init__(user_id)

    def course_set_up(self, name, time, instructor, size):
        conn = sqlite3.connect("gsz.db")
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

    def is_valid_applicant(self, applicant_id):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute("SELECT * FROM applicants WHERE applicant_id = ?", (applicant_id,))
        applicant_info = c.fetchone()
        conn.close()
        if applicant_info[7] == "student":
            # freshman doesn't have a GPA, so None is still acceptable
            return (applicant_info[4] > 3.0) or (applicant_info[4] == None)
        return False

    # if valid but deny, pop-up screen to type your reason

    def email_result(self, applicant_id, decision, justification):
        sender = "gradeschoolzero@gmail.com"
        password = "csc32200"
        port = 465
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            "SELECT email, first FROM applicants WHERE applicant_id = ?",
            (applicant_id,),
        )
        recipient = c.fetchone()
        subject = f"Hi {recipient[1]}, your application is reviewed"
        approve = "Welcome, you are approved :)"
        deny = "Sorry, you are not approved :("
        if decision == "approve":
            msg = f"Subject: {subject}\n\n{approve}"
            generated_id = generate_random()
            generated_password = generate_random()
            sql = "SELECT user_id FROM users WHERE user_id = ?"
            c.execute(sql, (generated_id,))
            while c.fetchone() != None:
                generated_id = generate_random()
                c.execute(sql, (generated_id,))
            msg += f"""\nYour id = {generated_id}\nYour password = {generated_password}\nPlease note that you need to change your passwor after your first login"""
            self.add_user(applicant_id, generated_id, generated_password)
        else:
            msg = f"Subject: {subject}\n\n{deny}"
            if justification != None:
                msg += f"\nthe reason is the following,\n{justification}"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient[0], msg)
        self.delete_applicant(applicant_id)

    def add_user(self, applicant_id, generated_id, generated_password):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "SELECT * FROM applicants WHERE applicant_id = ?"
        c.execute(sql, (applicant_id,))
        applicant_info = c.fetchone()
        sql = "INSERT INTO users(first, last, id, password, email, user_type, first_login) VALUES (?, ?, ?, ?, ?, ?, ?)"
        c.execute(
            sql,
            (
                applicant_info[1],
                applicant_info[2],
                generated_id,
                generated_password,
                applicant_info[3],
                applicant_info[7],
                1,
            ),
        )
        conn.commit()
        user_id = c.lastrowid
        if applicant_info[7] == "student":
            sql = """INSERT INTO students(user_id, gpa, honor_count, warning_count, num_courses_taken) VALUES (?, ?, ?, ?, ?)"""
            c.execute(sql, (user_id, applicant_info[4], 0, 0, applicant_info[4]))
        else:
            sql = "INSERT INTO instructors(user_id, warning_count, is_suspended) VALUES (?, ?, ?)"
            c.execute(sql, (user_id, 0, 0))
        conn.commit()
        conn.close()

    def delete_applicant(self, applicant_id):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "DELETE FROM applicants WHERE applicant_id = ?"
        c.execute(sql, (applicant_id,))
        conn.commit()
        conn.close()

    def deregister(self, course_id, student_id):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "UPDATE courses SET enroll_count = enroll_count - 1 WHERE course_id = ?"
        c.execute(sql, (course_id,))
        conn.commit()
        sql = "DELETE FROM enrollments WHERE student_id = ? AND course_id = ?"
        c.execute(sql, (student_id, course_id))
        conn.commit()
        conn.close()

    # ------- gui should show the table of complaints --------
    def process_complaints(self, complaint_id, decision):
        # approve
        # disapprove
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "SELECT complainant_id, complainee_id, complaint_type, course_id FROM complaints WHERE complaint_id = ?"
        c.execute(sql, (complaint_id,))
        complaint_info = c.fetchone()
        complaint_type = complaint_info[2]
        course_id = complaint_info[3]
        sql = "SELECT user_id, user_type FROM users WHERE user_id = ?"
        c.execute(sql, (complaint_info[0],))
        complainant_id_type = c.fetchone()
        c.execute(sql, (complaint_info[1],))
        complainee_id_type = c.fetchone()
        # student is complaining
        if complainant_id_type[1] == "student":
            # punish
            if decision == 1:
                # complain against student
                if complainee_id_type[1] == "student":
                    # update std db
                    sql = "UPDATE students SET warning_count = warning_count + 1 WHERE user_id = ?"
                    c.execute(sql, (complainee_id_type[0],))
                # complain against instructor
                else:
                    # update ins db
                    sql = "UPDATE instructors SET warning_count = warning_count + 1 WHERE user_id = ?"
                    c.execute(sql, (complainee_id_type[0],))
        # instructor is complaining
        else:
            # punish student
            if decision == 1:
                # warning
                if complaint_type == "warning":
                    # update std db
                    sql = "UPDATE students SET warning_count = warning_count + 1 WHERE user_id = ?"
                    c.execute(sql, (complainee_id_type[0],))
                # deregister
                else:
                    sql = "SELECT student_id FROM students WHERE user_id = ?"
                    c.execute(sql, (complainee_id_type[0],))
                    student_id = c.fetchone()[0]
                    self.deregister(course_id, student_id)
            # counter-punish instructor
            else:
                # warning
                sql = "UPDATE instructors SET warning_count = warning_count + 1 WHERE user_id = ?"
                c.execute(sql, (complainee_id_type[0]))
        conn.commit()
        # delete a row from complaint db
        sql = "DELETE FROM complaints WHERE complaint_id = ?"
        c.execute(sql, (complaint_id,))
        conn.commit()
        conn.close()


# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# reg1 = Registrar(1)
# reg1.email_result(1, 'approve', "a"
# reg1.email_result(2, 'approve', "b"
# reg1.email_result(3, 'approve', "c"
# reg1.email_result(4, 'approve', "d"
# reg1.email_result(5, 'approve', "e"
# conn.commit()
# conn.close()


class Student(User):
    def __init__(self, user_id):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE user_id = ?", (user_id,))
        student_info = c.fetchone()
        conn.close()
        super().__init__(student_info[1])
        self.student_id = student_info[0]
        self.gpa = student_info[2]
        self.num_courses_taken = student_info[3]
        self.honor_count = student_info[4]
        self.warning_count = student_info[5]
        # self.semester_gpa = student_info[6]
        # self.is_suspended = student_info[7]
        # self.degree = student_info[8]

    def is_time_conflict(self, course_id):
        conn = sqlite3.connect("gsz.db")
        # to get a list of values instead of a list of tuples
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        c.execute(
            "SELECT course_id FROM enrollments WHERE student_id=?", (self.student_id,)
        )
        courses = c.fetchall()
        c.execute(
            "SELECT course_time FROM courses WHERE course_id in ({courses})".format(
                courses=",".join(["?"] * len(courses))
            ),
            courses,
        )
        schedule = c.fetchall()
        schedule = [x.split(",") for x in schedule]
        schedule = [
            x2.replace(" - ", " ").strip().split(" ") for x1 in schedule for x2 in x1
        ]
        c.execute("SELECT course_time FROM courses WHERE course_id = ?", (course_id,))
        new_course = c.fetchone()
        new_course = new_course.split(",")
        new_course = [x.strip().replace(" - ", " ").split(" ") for x in new_course]
        for day in schedule:
            for new_day in new_course:
                if day[0] == new_day[0]:
                    if (not (day[1] > new_day[1])) and (not (day[2] < new_day[2])):
                        return True
        return False

    def is_too_many_courses(self):
        conn = sqlite3.connect("gsz.db")
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
        conn = sqlite3.connect("gsz.db")
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
        conn = sqlite3.connect("gsz.db")
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
        if not (self.is_eligible(course_id)):
            return 0
        if Course(course_id).is_full():
            self.apply_wait_list(course_id)
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "UPDATE courses SET enroll_count = enroll_count + 1 WHERE course_id = ?"
        c.execute(sql, (course_id,))
        conn.commit()
        sql = "INSERT INTO enrollments(student_id, course_id, grade) VALUES(?, ?, ?)"
        c.execute(sql, (self.student_id, course_id, None))
        conn.commit()
        conn.close()
        return 1

    # issue warning to student
    def receive_warning(self):
        new_warning_count = self.warning_count + 1
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """UPDATE student SET warning_count = :new_warning_count
                        WHERE student_id = student_id""",
            {"student_id": self.student_id, "new_warning_count": new_warning_count},
        )
        conn.commit()
        conn.close()

    # remove a warning from student class
    def remove_warning(self):
        new_warning_count = self.warning_count - 1
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """UPDATE student SET warning_count = :new_warning_count
                        WHERE student_id = student_id""",
            {"student_id": self.student_id, "new_warning_count": new_warning_count},
        )
        conn.commit()
        conn.close()

    # warn student for gpa btwn 2-2.25
    # student function
    def is_struggling(self):
        if 2 <= self.gpa <= 2.25:
            self.receive_warning()
            return True
        return False

    # if GPA < 2 or failed a course twice, if true then terminate
    def is_failing(self):
        if self.gpa < 2 or self.failed_twice():
            conn = sqlite3.connect("gsz.db")
            c = conn.cursor()
            c.execute("DELETE * FROM student WHERE student_id = ?", (self.student_id,))
            conn.commit()
            conn.close()
            return True
        return False

    # check to see if student failed class twice
    def failed_twice(self):
        failing_grade = 2.0  # or should it an 'F'
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """SELECT course_id FROM course_history WHERE grade < :failing_grade
                                    AND student_id =:student_id """,
            ({"failing_grade": failing_grade, "student_id": self.student_id}),
        )
        # if cousrse_id repeats return true else return false
        conn.commit()
        conn.close()

    # place student on honor roll if gpa > 3.5 or semester_gpa > 3.75
    def is_honor_roll(self):
        if self.gpa > 3.5 or self.semester_gpa > 3.75:
            self.remove_warning()
            self.place_honor_roll()
            return True
        return False

        # place honor_roll student on home page

    def place_honor_roll(self):
        # print(self.first, '? is on honor roll')
        pass

    # check if student can graduate
    def can_graduate(self):
        if self.num_courses_taken > 8:  # apply if classes taken >8
            self.apply_graduation()
            return True
        return False

    # apply for graduation, let registrar review
    def apply_graduation(self):
        # registrar needs to check if required courses passed
        # want to give some notification to registrar
        # print(self.first, '? applied to graduate')
        pass

    # reset semester grades (for end of period)
    @classmethod
    def reset_semester_grades(cls):
        semester_gpa = "NULL"
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """UPDATE students SET semester_gpa = :semester_gpa """,
            {"semester_gpa": semester_gpa},
        )
        conn.commit()
        conn.close()
        # update all students

    def complain(self, complainee_id, course_id, description):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "INSERT INTO complaints(complainant_id, course_id, complainee_id, description, complaint_type) VALUES(?, ?, ?, ?, ?)"
        c.execute(sql, (self.user_id, course_id, complainee_id, description, "warning"))
        conn.commit()
        conn.close()


class Instructor(User):
    def __init__(self, user_id):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute("SELECT * FROM instructors WHERE user_id = ?", (user_id,))
        instructor_info = c.fetchone()
        conn.close()
        super().__init__(instructor_info[1])
        self.instructor_id = instructor_info[0]
        self.warning_count = instructor_info[2]
        self.is_suspended = instructor_info[3]

    # suspend instructor automatically if warning count >=3
    def suspend(self):
        if self.warning_count >= 3:
            conn = sqlite3.connect("instructor.db")
            c = conn.cursor()
            c.execute(
                """UPDATE instructor SET is_suspended = :is_suspended
                                        WHERE instructor_id = :instructor_id""",
                {"instructor_id": self.instructor_id, "is_suspended": 1},
            )
            conn.commit()
            conn.close()
            # should warning_count be reset at start of semester?
            # how should is_suspended be reset

        # issue warning

    def receive_warning(self):
        new_warning_count = self.warning_count + 1
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """UPDATE instructor SET warning_count = :new_warning_count
                                WHERE instructor_id = instructor_id""",
            {
                "instructor_id": self.instructor_id,
                "new_warning_count": new_warning_count,
            },
        )
        conn.commit()
        conn.close()

    # assign grades to students during grading period
    def assign_grade(self, student, course, grade):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """UPDATE enrollments SET grade = :grade
                        WHERE student_id = :student_id
                        AND course_id =: course_id""",
            {
                "student_id": student.student_id,
                "course_id": course.course_id,
                "grade": grade,
            },
        )
        conn.commit()
        conn.close()

    # check if all students are graded, give warning otherwise
    def is_all_graded(self):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(
            """SELECT grade FROM enrollments
                        WHERE instructor_id =: instructor_id
                        AND grade IS NULL """,
            {"instructor_id": self.instructor_id},
        )
        conn.commit()
        if c.fetchall() == {}:
            conn.close()
            return True
        conn.close()
        self.recieve_warning()
        return False

    def complain(self, complainee_id, course_id, description, complaint_type):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        sql = "INSERT INTO complaints(complainant_id, course_id, complainee_id, description, complaint_type) VALUES(?, ?, ?, ?, ?)"
        c.execute(
            sql, (self.user_id, course_id, complainee_id, description, complaint_type)
        )
        conn.commit()
        conn.close()


# std1 = Student(6)
# std1.complain(7, 3, "too noisy")
# reg1 = Registrar(1)
# reg1.process_complaints(1, 1)
# reg1.process_complaints(2, 1)
# reg1.process_complaints(3, 1)
# Aiman

# reg1.process_complaints(9, 1)  # 9michael(instructor),8apple(student),de-register
# reg1.process_complaints(1, 0)  # 6david(student),7john(student),warning #worked
# reg1.process_complaints(2, 1)  # 7john(student),6david(student),warning #worked
# reg1.process_complaints(3, 1)  # 7john(student),9michael(instructor),warning #worked
# reg1.process_complaints(4, 1)  # 9michael(instructor),6david(student),warning #worked


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


# testing database

# # applicants table
# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS applicants(
#         applicant_id integer PRIMARY KEY,
#         first text NOT NULL,
#         last text NOT NULL,
#         email text NOT NULL,
#         gpa real,
#         resume text,
#         num_courses_taken integer,
#         user_type text NOT NULL
#         )"""
# )
# many_applicants = [
#     ("Kevin", "Durant", "gutiday14@gmail.com", "3.7", "None", 6, "student"),
#     ("Lebron", "James", "gutiday14@gmail.com", "2.7", "None", 6, "student"),
#     ("John", "Doe", "gutiday14@gmail.com", "5", None, 3, "student"),
#     (
#         "Jane",
#         "Doe",
#         "gutiday14@gmail.com",
#         None,
#         "I'm a good teacher",
#         None,
#         "instructor",
#     ),
#     ("Kevin", "Hart", "gutiday14@gmail.com", "3.7", "None", 6, "student"),
#     (
#         "Ashley",
#         "Doe",
#         "gutiday14@gmail.com",
#         None,
#         "I'm a bad teacher",
#         None,
#         "instructor",
#     ),
# ]
# c.executemany(
#     """INSERT INTO applicants(first, last, email, gpa, resume, num_courses_taken, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)""",
#     many_applicants,
# )
# conn.commit()
# conn.close()


# # users table
# conn = sqlite3.connect("gsz.db")
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
# many_users = [
#     ("Jane", "Doe", "ida5", "password", "email5@emgail.com", "instructor", 1),
#     ("Michael", "Jordan", "ida4", "password", "email4@email.com", "instructor", 1),
#     ("Apple", "Bee", "id13", "password", "email3@email.com", "student", 1),
#     ("John", "Doe", "idv2", "password", "email2@email.com", "student", 1),
#     ("David", "Beckham", "id1a", "password", "email1@email.com", "student", 1),
#     ("Kevin", "Durant", "Kevin_Durant@email.com", "3.7", "None", 6, "student"),
# ]
# c.executemany(
#     """INSERT INTO users(first, last, id, password, email, user_type, first_login) VALUES (?, ?, ?, ?, ?, ?, ?)""",
#     many_users,
# )
# conn.commit()
# conn.close()

# # complaints table
# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS complaints (
#         complaint_id integer PRIMARY KEY,
#         complainant_id integer NOT NULL,
#         complainee_id integer NOT NULL,
#         course_id integer NOT NULL,
#         description text NOT NULL,
#         complaint_type text,
#         FOREIGN KEY ('complainant_id') REFERENCES users (user_id),
#         FOREIGN KEY ('complainee_id') REFERENCES users (user_id),
#         FOREIGN KEY ('course_id') REFERENCES courses (course_id)
#         )"""
# )
# many_complaints = [
#     (9, 6, 3, "loud", "de-register"),
#     (9, 7, 3, "loud", "de-register"),
#     (9, 8, 3, "loud", "de-register"),
# ]
# c.executemany(
#     """INSERT INTO complaints(complainant_id, complainee_id, course_id, description, complaint_type) VALUES(?, ?, ?, ?, ?)""",
#     many_complaints,
# )
# conn.commit()
# conn.close()

# # students
# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE IF NOT EXISTS students (
#         student_id integer PRIMARY KEY,
#         user_id integer NOT NULL,
#         gpa real NOT NULL,
#         num_courses_taken integer NOT NULL,
#         honor_count integer NOT NULL,
#         warning_count integer NOT NULL,
#         semester_gpa real,
#         is_suspended integer NOT NULL,
#         degree text,
#         FOREIGN KEY ('user_id') REFERENCES users (user_id)
#         )"""
# )
# c.execute(
#     """INSERT INTO students(user_id, gpa, honor_count, warning_count, num_courses_taken, is_suspended) VALUES (?, ?, ?, ?, ?, ?)""",
#     (6, 5, 0, 0, 2, 0),
# )
# c.execute(
#     """INSERT INTO students(user_id, gpa, honor_count, warning_count, num_courses_taken, is_suspended) VALUES (?, ?, ?, ?, ?, ?)""",
#     (7, 3.5, 0, 0, 5, 0),
# )
# c.execute(
#     """INSERT INTO students(user_id, gpa, honor_count, warning_count, num_courses_taken, is_suspended) VALUES (?, ?, ?, ?, ?, ?)""",
#     (8, 2.8, 0, 0, 3, 0),
# )
# conn.commit()
# conn.close()

# # instructors table
# conn = sqlite3.connect("gsz.db")
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
#     (9, 0, 0),
# )
# c.execute(
#     """INSERT INTO instructors(user_id, warning_count, is_suspended) VALUES (?, ?, ?)""",
#     (10, 0, 0),
# )
# conn.commit()
# conn.close()

# # courses table
# conn = sqlite3.connect("gsz.db")
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

# # enrollments table
# conn = sqlite3.connect("gsz.db")
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
#         6,
#         3,
#         None,
#     ),
# )
# c.execute(
#     """INSERT INTO enrollments(student_id, course_id, grade) VALUES (?, ?, ?)""",
#     (
#         7,
#         3,
#         None,
#     ),
# )
# conn.commit()
# conn.close()


# # enrollments table
# conn = sqlite3.connect("gsz.db")
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
# many_enrollments = [
#     (1, 3, None),
#     (2, 3, None),
#     (3, 3, None),
# ]
# c.executemany(
#     """INSERT INTO enrollments(student_id, course_id, grade) VALUES (?, ?, ?)""",
#     many_enrollments,
# )
# conn.commit()
# conn.close()


# # course_historys table
# conn = sqlite3.connect("gsz.db")
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

# # waitlists table
# conn = sqlite3.connect("gsz.db")
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
# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# c.execute("SELECT * FROM users WHERE user_id=1")
# args = c.fetchone()
# reg1 = Registrar(args[0])
# c.execute("SELECT * FROM instructors WHERE instructor_id=1")
# args = c.fetchone()
# instructor1 = Instructor(args[0])
# reg1.course_set_up("CSC 33500", "Tu 12:00 - 1:15, We 12:00 - 2:30", args[0], 25)


# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# c.execute("SELECT * FROM students WHERE student_id=?", (1,))
# args = c.fetchone()
# student1 = Student(args[0])
# print(student1.apply_wait_list(3))
# print(student1.apply_wait_list(4))
# print(student1.apply_wait_list(5))
# print(student1.apply_wait_list(6))

# # update a row
# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# # sql = """UPDATE applicants SET first = ?, last = ? WHERE applicant_id = ?"""
# sql = """UPDATE applicants SET approval_status = ?"""
# # c.execute(sql, ("Jane_Doe@email.com", 2))
# # c.execute(sql, ("Cristiano_Ronaldo@email.com", 3))
# # c.execute(sql, ("James_Miler@email.com", 6))
# # c.execute(sql, ("David_Villa@email.com", 7))
# conn.commit()
# conn.close()

# delete a row
# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# sql = """DELETE FROM applicants WHERE applicant_id = ?"""
# c.execute(sql, (6,))
# c.execute(sql, (13,))
# c.execute(sql, (14,))
# c.execute(sql, (15,))
# c.execute(sql, (16,))
# c.execute(sql, (17,))
# conn.commit()
# conn.close()

# # delete a row
# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# sql = """DELETE FROM enrollments"""
# c.execute(sql)
# conn.commit()
# conn.close()


# # add a column
# sql = "ALTER TABLE applicants ADD approval_status text"
# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# c.execute(sql)
# conn.commit()
# conn.close()

# # delete a table
# sql = "DROP TABLE reviews"
# conn = sqlite3.connect("gsz.db")
# c = conn.cursor()
# c.execute(sql)
# conn.commit()
# conn.close()
