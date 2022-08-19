from datetime import datetime
from mashov_api import login_request, create_timetable


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def error(s: str):
    """
    Print error with colorful and then exit with return code of -1
    """
    print(bcolors.FAIL + s + bcolors.ENDC + "\n")
    exit(-1)

INPUT_DATETIME_FORMAT = "%Y %m %d"

def main() -> None:
    try:
        r = login_request(input("Username? "), input("Password? "),
             int(input("Semel? ")), int(input("Year? ")))
    except Exception as e:
        error(e.__str__())
        
    print(F"{bcolors.OKGREEN}Successfully logged in...{bcolors.ENDC}\n")
    print(F"{bcolors.WARNING}! RECOMMENDED: - NO MORE THAN A MONTH DUE TO TIMETABLE CHANGES{bcolors.ENDC}")

    try:
        d1 = datetime.strptime(input(F"Calender first day date? (Year Month Day): "), INPUT_DATETIME_FORMAT)
        d2 = datetime.strptime(input(F"Calender last day date? (Year Month Day): "), INPUT_DATETIME_FORMAT)

        create_timetable(d1, d2, r) 
    except Exception as e:
        error(e.__str__())

    print(F"{bcolors.OKBLUE}Finished! " +
            F"Check the current folder for file named {bcolors.UNDERLINE + bcolors.BOLD}\"timetable.ics\"{bcolors.ENDC}")

if __name__ == "__main__":
    main()
