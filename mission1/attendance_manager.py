player_info = {}

# attendance_info[사용자ID][요일]
attendance_info = [[0] * 100 for _ in range(100)]
points = [0] * 100
grade = [''] * 100
names = [''] * 100
attendance_count_training = [0] * 100
attendance_count_weekend = [0] * 100

def get_player_id(player):
    return player_info[player]

def set_player_info(player_name):
    player_id = len(player_info) + 1
    player_info[player_name] = player_id
    names[player_id] = player_name

def reflect_attendance_info(player_name, day):
    player_id = get_player_id(player_name)
    day_index = get_day_index(day)
    attendance_info[player_id][day_index] += 1

    if day_index == 2:
        attendance_count_training[player_id] += 1

    if day_index in [5, 6]:
        attendance_count_weekend[player_id] += 1

def calculate_player_points():
    for player_name, player_id in player_info.items():
        point = 0

        for day_index in range(7):
            point += attendance_info[player_id][day_index] * get_day_point(day_index)

        point += get_bonus_point(player_id)
        points[player_id] += point

def get_grade(point):
    if point >= 50:
        return "GOLD"
    elif point >= 30:
        return "SILVER"
    else:
        return "NORMAL"

def set_player_grade():
    for player_name, player_id in player_info.items():
        grade[player_id] = get_grade(points[player_id])

def get_day_point(day_index):
    if day_index == 2:
        return 3  # wednesday
    elif day_index in [5, 6]:
        return 2  # weekend
    else:
        return 1  # other weekday

def get_bonus_point(player_id):
    point = 0
    point += 10 if attendance_count_training[player_id] >= 10 else 0
    point += 10 if attendance_count_weekend[player_id] >= 10 else 0
    return point

def get_day_index(day):
    day_index_map = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    return day_index_map[day]

def get_attendance_list_from_file():
    attendance_list = []
    with open("attendance_weekday_500.txt", encoding='utf-8') as f:
        for _ in range(500):
            line = f.readline()
            if not line:
                break

            parts = line.strip().split()
            player_name = parts[0]
            day = parts[1]

            if len(parts) == 2:
                attendance_list.append((player_name, day))

    return attendance_list


def set_attendance_data():
    attendance_list = get_attendance_list_from_file()

    for player_name, day in attendance_list:
        if player_name not in player_info:
            set_player_info(player_name)

        reflect_attendance_info(player_name, day)

def get_withdraw_candi_list():
    withdraw_candi_list = []
    for player_name, player_id in player_info.items():
        if (grade[player_id] == "NORMAL" 
                and attendance_count_training[player_id] == 0 
                and attendance_count_weekend[player_id] == 0):
            withdraw_candi_list.append(player_name)

    return withdraw_candi_list

def set_attendance_info_from_file():
    set_attendance_data()
    calculate_player_points()
    set_player_grade()

def print_attendance_summary():
    for player_name, player_id in player_info.items():
        print(f"NAME : {player_name}, POINT : {points[player_id]}, GRADE : {grade[player_id]}")

    print("\nRemoved player")
    print("==============")

    withdraw_candi_list = get_withdraw_candi_list()
    for player_name in withdraw_candi_list:
        print(player_name)


if __name__ == "__main__":
    set_attendance_info_from_file()
    print_attendance_summary()
