def get_attendance_list_from_file(file_path):
    try:
        attendance_list = []

        with open(file_path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    attendance_list.append((parts[0], parts[1]))

        return attendance_list
    except FileNotFoundError:
        print(f"FileNotFoundError : {file_path}")