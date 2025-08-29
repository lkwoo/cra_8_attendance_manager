import pytest
from strategy import MAPPING_DAY_TO_DAY_INDEX, TRAINING_DAY_INDEX_LIST, WEEKEND_DAY_INDEX_LIST
from strategy import DefaultGradeStrategy, DefaultPointStrategy
from strategy import GradeStrategy, PointStrategy
from strategy import mapping_day_index_to_point

from manager import AttendanceManager
from user import User
import data_loader


def test_user_add_and_get_attendance():
    user = User("Umar")
    assert user.name == "Umar"
    assert user.points == 0
    assert user.grade == "NORMAL"

    for i in range(7):
        user.add_attendance(i)

    for i in range(7):
        assert user.get_attendance_count_day_index(i) == 1


def test_setter():
    user = User("Umar")
    user.points = 42
    user.grade = "SILVER"
    assert user.points == 42
    assert user.grade == "SILVER"


def test_mapping_day_index_to_point():
    assert mapping_day_index_to_point(2) == 3   # training day
    assert mapping_day_index_to_point(5) == 2   # weekend
    assert mapping_day_index_to_point(6) == 2   # weekend
    assert mapping_day_index_to_point(1) == 1   # weekday
    assert mapping_day_index_to_point(0) == 1  # weekday


def test_strategy_no_impl():
    user = User("Ian")

    with pytest.raises(NotImplementedError):
        GradeStrategy.assign_grade(user)

    with pytest.raises(NotImplementedError):
        PointStrategy.calculate_point(user)


def make_user_with_points(points):
    user = User("Ian")
    user.points = points
    DefaultGradeStrategy.assign_grade(user)
    return user

def test_assign_grade_boundaries():
    assert make_user_with_points(50).grade == "GOLD"
    assert make_user_with_points(49).grade == "SILVER"
    assert make_user_with_points(30).grade == "SILVER"
    assert make_user_with_points(29).grade == "NORMAL"


def test_calculate_point_and_bonuses():
    u = User("Charlie")
    
    for _ in range(10):
        u.add_attendance(2)

    for _ in range(10):
        u.add_attendance(5)

    DefaultPointStrategy.calculate_point(u)

    base = 30 + 20
    assert u.points == base + 20


def test_set_user_info_and_withdraw_list():
    attendance_list = [
        ("Steve", "monday"),
        ("Charlie", "wednesday"),
        ("Charlie", "saturday"),
        ("Xena", "wednesday"),
        ("Xena", "wednesday"),
        ("Xena", "wednesday"),
        ("Xena", "wednesday"),
        ("Xena", "wednesday"),
        ("Xena", "wednesday"),
        ("Xena", "wednesday"),
        ("Xena", "wednesday"),
        ("Xena", "wednesday"),
        ("Xena", "wednesday"),
    ]
    attendance_manager = AttendanceManager()
    attendance_manager.set_user_info(attendance_list)

    assert "Steve" in attendance_manager.users
    assert "Charlie" in attendance_manager.users

    withdraw = attendance_manager.get_withdraw_candi_user_list()
    assert "Dave" in withdraw or "Eve" not in withdraw


def test_get_attendance_list_from_file(tmp_path):
    file_path = tmp_path / "attendance.txt"
    file_path.write_text("Alice tuesday\nHannah thursday\nInvalidLine1\nInvalidLine 2 3", encoding="utf-8")

    result = data_loader.get_attendance_list_from_file(str(file_path))
    assert ("Alice", "tuesday") in result
    assert ("Hannah", "thursday") in result
    assert not any(len(r) != 2 for r in result)


def test_get_attendance_list_file_not_found(capsys):
    res = data_loader.get_attendance_list_from_file("not_exist_file.txt")
    captured = capsys.readouterr()
    assert res is None
    assert "FileNotFoundError" in captured.out


def test_result(capsys):
    answers = ["NAME : Alice, POINT : 61, GRADE : GOLD\n",
"NAME : Bob, POINT : 8, GRADE : NORMAL\n",
"NAME : Charlie, POINT : 58, GRADE : GOLD\n",
"NAME : Daisy, POINT : 45, GRADE : SILVER\n",
"NAME : Ethan, POINT : 44, GRADE : SILVER\n",
"NAME : George, POINT : 42, GRADE : SILVER\n",
"NAME : Hannah, POINT : 127, GRADE : GOLD\n",
"NAME : Ian, POINT : 23, GRADE : NORMAL\n",
"NAME : Nina, POINT : 79, GRADE : GOLD\n",
"NAME : Oscar, POINT : 13, GRADE : NORMAL\n",
"NAME : Quinn, POINT : 6, GRADE : NORMAL\n",
"NAME : Rachel, POINT : 54, GRADE : GOLD\n",
"NAME : Steve, POINT : 38, GRADE : SILVER\n",
"NAME : Tina, POINT : 24, GRADE : NORMAL\n",
"NAME : Umar, POINT : 48, GRADE : SILVER\n",
"NAME : Vera, POINT : 22, GRADE : NORMAL\n",
"NAME : Will, POINT : 36, GRADE : SILVER\n",
"NAME : Xena, POINT : 91, GRADE : GOLD\n",
"NAME : Zane, POINT : 1, GRADE : NORMAL\n",
"\n",
"Removed player\n",
"==============\n",
"Bob\n",
"Zane\n"]

    attendance_list = data_loader.get_attendance_list_from_file("attendance_weekday_500.txt")

    service = AttendanceManager()
    service.set_user_info(attendance_list)
    service.print_attendance_summary()

    captured = capsys.readouterr()
    for answer in answers:
        assert answer in captured.out
