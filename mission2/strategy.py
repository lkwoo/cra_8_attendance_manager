MAPPING_DAY_TO_DAY_INDEX = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
}
TRAINING_DAY_INDEX_LIST = [2]
WEEKEND_DAY_INDEX_LIST = [5, 6]

def mapping_day_index_to_point(day_index):
    if day_index in TRAINING_DAY_INDEX_LIST:
        return 3
    elif day_index in WEEKEND_DAY_INDEX_LIST:
        return 2
    else:
        return 1


class PointStrategy:
    @staticmethod
    def calculate_point(user):
        raise NotImplementedError

class DefaultPointStrategy(PointStrategy):
    @staticmethod
    def calculate_point(user):
        user.points = 0

        # Default Point
        for day_index in range(7):
            user.points += user.attendance[day_index] * mapping_day_index_to_point(day_index)

        # Bonus Points
        training_attendance_sum = 0
        weekend_attendance_sum = 0

        for training_day_index in TRAINING_DAY_INDEX_LIST:
            training_attendance_sum += user.get_attendance_count_day_index(training_day_index)

        for weekend_day_index in WEEKEND_DAY_INDEX_LIST:
            weekend_attendance_sum += user.get_attendance_count_day_index(weekend_day_index)

        if training_attendance_sum >= 10:
            user.points += 10

        if weekend_attendance_sum >= 10:
            user.points += 10


class GradeStrategy:
    @staticmethod
    def assign_grade(user):
        raise NotImplementedError


class DefaultGradeStrategy(GradeStrategy):
    @staticmethod
    def assign_grade(user):
        if user.points >= 50:
            user.grade = "GOLD"
        elif user.points >= 30:
            user.grade = "SILVER"
        else:
            user.grade = "NORMAL"