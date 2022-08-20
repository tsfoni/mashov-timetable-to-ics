# Written by Harel Tsfoni (bizz.harel@gmail.com)

from datetime import datetime, time, timedelta
import requests

API_JSON_URL = "https://web.mashov.info/api/students/"
API_JSON_LESSONS_TIME_URL = "https://web.mashov.info/api/bells"
DEFAULT_FORMAT_TIME = "%H:%M:%S"

# Convert Mashov json weekdays numbers to Datetime weekdays numbers
# e.g: at '1' (Sunday in Mashov format) will be '6' (Sunday in Datetime format)
days_of_week = {
    1: 6,
    2: 0,
    3: 1,
    4: 2,
    5: 3,
    6: 4,
    7: 5
}   

class lesson:
    """
    Details about the lessons
    """
    def __init__(self, name: str, room: str, teachers: list, weekday: int,
                lesson_number: str, starts: time, ends: time ) -> None:
        self.name = name
        self.room = room
        self.teachers = teachers
        self.weekday = weekday
        self.lesson_number = lesson_number
        self.starts = starts
        self.ends = ends

class timetable:
    def __init__(self, owner_name: str) -> None:
        self.owner_name = owner_name
        self.lessons = []

    def add_lesson(self, lesson: lesson):
        self.lessons.append(lesson)

def lesson_time_to_dict(lessons_time_json) -> dict:
    """
    Convert the json dictionary format to simplifed dictionary
    """
    lessons = { }
    for lesson in lessons_time_json:
        lessons[lesson["lessonNumber"]] = {
            "startTime": datetime.strptime(lesson["startTime"],
                            DEFAULT_FORMAT_TIME).time(),
            "endTime": datetime.strptime(lesson["endTime"], 
                            DEFAULT_FORMAT_TIME).time()
        }
    return lessons

def fetch_teachers(lesson: dict) -> list:
    names = []

    for teacher in lesson["groupDetails"]["groupTeachers"]:
        names.append(teacher["teacherName"])

    return names    

def fetch_timetable(mashov_login_details: requests.Response) -> timetable:
    h = {
      "x-csrf-token": mashov_login_details.headers["x-csrf-token"]
    }

    user_info = mashov_login_details.json()

    lessons = requests.get(API_JSON_URL + (user_info["credential"])["userId"] 
    + "/timetable", headers=h, cookies=mashov_login_details.cookies).json()

    lessons_times = lesson_time_to_dict(requests.get(API_JSON_LESSONS_TIME_URL, headers=h, 
                cookies=mashov_login_details.cookies).json())

    _timetable = timetable(user_info["credential"]["displayName"])
    
    for _lesson in lessons:
        _timetable.add_lesson(
            lesson(_lesson["groupDetails"]["subjectName"],
                _lesson["timeTable"]["roomNum"], fetch_teachers(_lesson),
                days_of_week[_lesson["timeTable"]["day"]], 
                _lesson["timeTable"]["lesson"], 
                lessons_times[_lesson["timeTable"]["lesson"]]["startTime"],
                lessons_times[_lesson["timeTable"]["lesson"]]["endTime"]
            )
        )

    
    return _timetable




