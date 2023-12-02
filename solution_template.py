from datetime import datetime

import sys
sys.path.append("../modules/")
import input_parsing

INPUT_FILES_DIR = "../data/"


def todays_month_day(padding_target_length: int = 2) -> str:
    """Return a 0-padded number of the current day of the month.
    Used to get the number of the current date within the advent calendar"""
    return str(datetime.today().date().day).zfill(padding_target_length)


if __name__ == "__main__":
    data = input_parsing.load_list_of_strings(f"{INPUT_FILES_DIR}{todays_month_day(2)}-input")
    print(data)
