"""
periods module makes sure the periods don't overlap each other
while you are initializing or updating them
"""
import datetime


class Period:
    """
    Period class consists of four periods.
    All periods should be datetime objects.
    """

    def __init__(self, class_set_up, course_registration, class_running, grading):
        self.check(class_set_up, course_registration, class_running, grading)
        self.class_set_up = class_set_up
        self.course_registration = course_registration
        self.class_running = class_running
        self.grading = grading

    def check(self, class_set_up, course_registration, class_running, grading):
        """
        check if there is overlap or use of invalid datatype
        """
        temp = [
            class_set_up,
            course_registration,
            class_running,
            grading,
        ]
        # check if each period is a list of datetime of length 2 or start date < end date
        for x in temp:
            if (
                (not isinstance(x, list))
                or (len(x) != 2)
                or (not isinstance(x[0], datetime.date))
                or (not isinstance(x[1], datetime.date))
            ):
                raise Exception(
                    "All periods should be a list of datetime of length 2. Update/initilization failed!"
                )
            if x[0] >= x[1]:
                raise Exception(
                    "End date of a period should come after start date of a period. Update/initilization failed!"
                )
        # check for overlaps
        if (
            (class_set_up[1] >= course_registration[0])
            or (course_registration[1] >= class_running[0])
            or (class_running[1] >= grading[0])
            # p1 = [datetime.date(2022, 9, 1), datetime.date(2022, 9, 2)]
            # p2 = [datetime.date(2022, 9, 2), datetime.date(2022, 9, 4)]
            # p3 = [datetime.date(2022, 9, 5), datetime.date(2022, 9, 6)]
            # p4 = [datetime.date(2022, 9, 7), datetime.date(2022, 9, 8)]
        ):
            raise Exception(
                "There is one or more overlap in the periods. Update/initilization failed!"
            )
        return 1

    def set_class_set_up(self, new_class_set_up):
        if (
            self.check(
                new_class_set_up,
                self.course_registration,
                self.class_running,
                self.grading,
            )
            == -1
        ):
            return
        else:
            self.class_set_up = new_class_set_up

    def set_course_registration(self, new_course_registration):
        if (
            self.check(
                self.class_set_up,
                new_course_registration,
                self.class_running,
                self.grading,
            )
            == -1
        ):
            return
        else:
            self.class_set_up = new_course_registration

    def set_class_running(self, new_class_running):
        if (
            self.check(
                self.class_set_up,
                self.course_registration,
                new_class_running,
                self.grading,
            )
            == -1
        ):
            return
        else:
            self.class_set_up = new_class_running

    def set_grading(self, new_grading):
        if (
            self.check(
                self.class_set_up,
                self.course_registration,
                self.class_running,
                new_grading,
            )
            == -1
        ):
            return
        else:
            self.class_set_up = new_grading


# # for testing
# p1 = [datetime.date(2022, 9, 1), datetime.date(2022, 9, 2)]
# p2 = [datetime.date(2022, 9, 2), datetime.date(2022, 9, 4)]
# p3 = [datetime.date(2022, 9, 5), datetime.date(2022, 9, 6)]
# p4 = [datetime.date(2022, 9, 7), datetime.date(2022, 9, 8)]
# period = Period(p1, p2, p3, p4)
# print(period.class_set_up)
# print(period.course_registration)
# print(period.class_running)
# print(period.grading)
