from manager import AttendanceManager
from data_loader import get_attendance_list_from_file


attendance_list = get_attendance_list_from_file("attendance_weekday_500.txt")

service = AttendanceManager()
service.set_user_info(attendance_list)
service.print_attendance_summary()


