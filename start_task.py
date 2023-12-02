from datetime import datetime
import shutil
import sys
import requests
import webbrowser


INPUT_FILES_DIR = "./data/"
SOLUTION_FILES_DIR = "./src/"
TEMPLATE_FILE_PATH = "solution_template.py"
LOGIN_URL = "https://adventofcode.com/2023/auth/login"


def download_input_file(
        url: str,
        dest_file_path: str,
        session_cookie: str) -> int:
    """Returns status code"""
    cookie_dict = {"session": session_cookie}
    s = requests.Session()
    s.post(LOGIN_URL, {"session": session_cookie})
    with requests.get(url, stream=True, cookies=cookie_dict) as request:
        with open(dest_file_path, "w") as fp:
            fp.write(request.content.decode())
        status_code = request.status_code
    return status_code


def todays_month_day(padding_target_length: int = 2):
    """Return a 0-padded number of the current day of the month.
    Used to get the number of the current date within the advent calendar"""
    return str(datetime.today().date().day).zfill(padding_target_length)


def task_url_from_day(day_number: int) -> str:
    return f"https://adventofcode.com/2023/day/{day_number}"


def input_url_from_day(day_number: int) -> str:
    return f"https://adventofcode.com/2023/day/{day_number}/input"


if __name__ == "__main__":
    # pass authentication session cookie as the only command argument
    # finding it in firefox: enter the development tools (F12 or ctrl+shift+I)
    # and go to Storage, and select "Cookies" on the left pane
    # find the cookie "session" on the list that appears
    session_cookie = sys.argv[1]
    day_str = todays_month_day(1)
    padded_day_str = todays_month_day(2)
    input_url = input_url_from_day(day_str)
    input_path = f"{INPUT_FILES_DIR}{padded_day_str}-input"
    download_input_file(input_url, input_path, session_cookie)

    # open the page with problem description
    webbrowser.open(task_url_from_day(todays_month_day(1)))
    shutil.copy(TEMPLATE_FILE_PATH, f"{SOLUTION_FILES_DIR}day{padded_day_str}.py")
