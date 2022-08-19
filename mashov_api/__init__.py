# Written by Harel Tsfoni

import requests
from datetime import datetime, timedelta
from ics import Calendar, Event
from pytz import timezone
from .timetable import fetch_timetable, lesson, timetable

LOGIN_URL = "https://web.mashov.info/api/login"


def login_request(username: str, password: str, semel: int, year: int) -> requests.Response:
    login_info = {"semel": semel, "year": year, "username": username, 
    "password": password, "IsBiometric": False, "deviceUuid": "Harel Tsfoni Script"}

    _request = requests.post(LOGIN_URL, json=login_info)

    if _request.status_code == 401:
        raise Exception("Incorrect password or username.")
    elif _request.status_code != 200:
        raise Exception("Something went wrong, check all fields for incorrect data.")

    return _request
 

def get_closest_date(date: datetime, weekday: int) -> datetime:
    """
    Calculates the closest date to date by weekday (In the same day or after)
    """

    newDate = date
    while newDate.weekday() != weekday:
        newDate += timedelta(1)

    return newDate



def create_timetable(begins: datetime, ends: datetime, login_details: requests.Response) -> None:
    timetable = fetch_timetable(login_details)
    c = Calendar()
    c.creator = "Mashov Time-table API - By Harel Tsfoni"

    uid_counter = 0
    for lesson in timetable.lessons:
        e = Event(lesson.name)

        e.description = "חדר: " + lesson.room + "\n"
        e.description += "מורים: \n"
        for teacherName in lesson.teachers:
            e.description += "\t- " + teacherName + "\n"

        lesson_date = get_closest_date(begins, lesson.weekday) # The first lesson

        while lesson_date <= ends:
            lesson_date_time = e.clone()
            
            lesson_date_time.uid = F"LESSON{uid_counter}"

            lesson_date_time.begin = timezone('Asia/Jerusalem').localize(datetime(
            lesson_date.year, lesson_date.month, lesson_date.day,
            lesson.starts.hour, lesson.starts.minute)).isoformat()

            lesson_date_time.end = timezone('Asia/Jerusalem').localize(datetime(
            lesson_date.year, lesson_date.month, lesson_date.day,
            lesson.ends.hour, lesson.ends.minute)).isoformat()
            
            c.events.add(lesson_date_time)
            lesson_date += timedelta(7) # Next week
            
            uid_counter += 1


    with open('timetable.ics', 'w', encoding='utf-8') as file:
        file.writelines(c.serialize_iter())

