class User:
    def __init__(self, name):
        self.name = name
        self.attendance = [0] * 7
        self.points = 0
        self.grade = "NORMAL"

    def add_attendance(self, day_index: int):
        self.attendance[day_index] += 1

    def get_attendance_count_day_index(self, day_index: int):
        return self.attendance[day_index]

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, grade):
        self._grade = grade

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points