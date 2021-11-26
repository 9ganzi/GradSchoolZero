import sqlite3


class Course:
    def __init__(self, course_id):
        conn = sqlite3.connect("course.db")
        c = conn.cursor()
        c.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
        course_info = c.fetchone()
        conn.close()
        self.course_id = course_info[0]
        self.course_name = course_info[1]
        self.course_rating = course_info[2]
        self.course_time = course_info[3]
        self.instructor_id = course_info[4]
        self.course_size = course_info[5]
        self.enroll_count = course_info[6]
        self.course_gpa = course_info[7]
