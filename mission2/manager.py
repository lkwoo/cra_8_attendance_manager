from user import User
from strategy import MAPPING_DAY_TO_DAY_INDEX, TRAINING_DAY_INDEX_LIST, WEEKEND_DAY_INDEX_LIST
from strategy import DefaultGradeStrategy, DefaultPointStrategy


class AttendanceManager:
    def __init__(self):
        self.users = {}

    def set_user_info(self, attendance_list):
        for name, day in attendance_list:
            if name not in self.users:
                self.users[name] = User(name)

            self.users[name].add_attendance(MAPPING_DAY_TO_DAY_INDEX[day])

        for user in self.users.values():
            DefaultPointStrategy.calculate_point(user)
            DefaultGradeStrategy.assign_grade(user)

    def get_withdraw_candi_user_list(self):
        withdraw_candi_user_list = []

        for user in self.users.values():
            if user.grade != "NORMAL":
                continue

            special_day_attendance_count = 0
            for day_index in TRAINING_DAY_INDEX_LIST:
                special_day_attendance_count += user.get_attendance_count_day_index(day_index)

            for day_index in WEEKEND_DAY_INDEX_LIST:
                special_day_attendance_count += user.get_attendance_count_day_index(day_index)

            if special_day_attendance_count == 0:
                withdraw_candi_user_list.append(user.name)

        return withdraw_candi_user_list

    def print_attendance_summary(self):
        for user in self.users.values():
            print(f"NAME : {user.name}, POINT : {user.points}, GRADE : {user.grade}")

        print("\nRemoved player")
        print("==============")
        for name in self.get_withdraw_candi_user_list():
            print(name)

