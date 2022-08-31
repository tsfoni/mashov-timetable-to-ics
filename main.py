from datetime import datetime
from mashov_api import login_request, create_timetable

def error(s: str):
    """
    Print error and then exit with return code of -1
    """
    input(s)
    exit(-1)

INPUT_DATETIME_FORMAT = "%Y %m %d"

def main() -> None:
    try:
        r = login_request(input("Username? "), input("Password? "),
             int(input("Semel? ")), int(input("Year? ")))
    except Exception as e:
        error(e.__str__())
        
    print("Successfully logged in...\n")
    print("! RECOMMENDED: - NO MORE THAN A MONTH DUE TO TIMETABLE CHANGES")

    try:
        d1 = datetime.strptime(input(F"Calender first day date? (Year Month Day): "), INPUT_DATETIME_FORMAT)
        d2 = datetime.strptime(input(F"Calender last day date? (Year Month Day): "), INPUT_DATETIME_FORMAT)

        timetable = create_timetable(d1, d2, r) 
    except Exception as e:
        error(e.__str__())

    if len(timetable.fails) > 0:
        print("\nI could not add these lessons:")
        for fail in timetable.fails:
            print("\t -" + fail.__str__())

    input("\nFinished! Check the current folder for file named \"timetable.ics\"")

if __name__ == "__main__":
    main()