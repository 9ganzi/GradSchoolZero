import sqlite3


# ensure Course gpa btwn 2.5 -3.5
def is_fair():
    conn = sqlite3.connect("gsz.db")
    c = conn.cursor() # assume all classes are fair at start
    c.execute(""" UPDATE courses SET is_fair = False WHERE course_gpa NOT BETWEEN 2.5 AND 3.5 """)
    conn.commit()
    conn.close()

class Course:
    def __init__(self, course_id):
        conn = sqlite3.connect("gsz.db")
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

    def is_full(self):
        return self.enroll_count >= self.course_size

    
    # take average of all grades then set that to course_gpa
    def calculate_course_gpa(self):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute(""" SELECT avg(grade) From enrollments WHERE course_id : course_id """,
                               {'course_id': self.course_id})
        course_gpa = c.fetchone()[0]
        
        c.execute(""" UPDATE courses SET course_gpa = :course_gpa
                                WHERE course_id = course_id""",
                  {'course_id': self.course_id, 'course_gpa': course_gpa})
        conn.commit()
        c.close()
        
   # reset course info at end of semester
    @classmethod
    def reset_courses(cls):
        conn = sqlite3.connect("gsz.db")
        c = conn.cursor()
        c.execute("""UPDATE student SET semester_gpa = :semester_gpa, 
                    enroll_count = :enroll_count,
                    is_fair =: is_fair""",
                  {'semester_gpa': 0, 'enroll_count': 0, 'is_fair': 'True'})
        conn.commit()
        conn.close()
