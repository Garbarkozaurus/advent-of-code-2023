from datetime import datetime
import re

import sys
sys.path.append("../modules/")
import input_parsing

INPUT_FILES_DIR = "../data/"

# PART 2 not done


def todays_month_day(padding_target_length: int = 2) -> str:
    """Return a 0-padded number of the current day of the month.
    Used to get the number of the current date within the advent calendar"""
    return str(datetime.today().date().day).zfill(padding_target_length)


def number_starts_and_ends(line: str) -> list[tuple[int, int]]:
    ret = []
    within_number = False
    number_start = None
    for i, c in enumerate(line):
        if c.isdigit():
            if not within_number:
                within_number = True
                number_start = i
            else:
                continue
        elif within_number:
            within_number = False
            number_end = i - 1
            ret.append((number_start, number_end))
    # to include numbers that end at the end of the line
    if within_number:
        ret.append((number_start, len(line)-1))
    return ret


IGNORED_CHARACTERS = set(list(".0123456789"))


def is_section_part_number(start: int, end: int, line: str, line_len: int,
                           check_range: bool):
    if start > 0:
        if line[start-1] not in IGNORED_CHARACTERS:
            return True

    if end < line_len - 1:
        if line[end+1] not in IGNORED_CHARACTERS:
            return True
    if check_range:
        for i in range(start, end+1):
            if line[i] not in IGNORED_CHARACTERS:
                return True
    return False


def sum_part_numbers_in_line(line_number: int, schematic: list[str], line_len: int):
    offsets_to_check = (-1, 0, 1)
    if line_number == 0:
        offsets_to_check = (0, 1)
    if line_number == len(schematic) - 1:
        offsets_to_check = (-1, 0)
    starts_ends = number_starts_and_ends(schematic[line_number])
    line_sum = 0
    for (start, end) in starts_ends:
        part_number = None
        for offset in offsets_to_check:
            if is_section_part_number(start, end, schematic[line_number+offset], line_len, bool(offset != 0)):
                part_number = int(schematic[line_number][start:end+1])
                break
        if part_number is not None:
            line_sum += part_number
    return line_sum


def sum_part_numbers_in_schematic(schematic: list[str]):
    # process the first line
    width = len(schematic[0])
    part_sum = 0
    for i in range(len(schematic)):
        part_sum += sum_part_numbers_in_line(i, schematic, width)
        if i == 126:
            s_e = number_starts_and_ends(schematic[i])
            print(schematic[i][s_e[-1][0]:s_e[-1][1]+1])
            print(schematic[i][128])
    return part_sum


def get_part_numbers_in_line(schematic: list[str], line_number: int,
                             line_len: int) -> list[tuple[int, int]]:
    offsets_to_check = (-1, 0, 1)
    if line_number == 0:
        offsets_to_check = (0, 1)
    if line_number == len(schematic) - 1:
        offsets_to_check = (-1, 0)
    starts_ends = number_starts_and_ends(schematic[line_number])
    part_number_starts_ends = []
    for (start, end) in starts_ends:
        for offset in offsets_to_check:
            if is_section_part_number(start, end, schematic[line_number+offset], line_len, bool(offset != 0)):
                part_number_starts_ends.append((start, end))
    return part_number_starts_ends


def is_asterisk_gear(position: int, line_number: int,
                     starts_ends: list[list[tuple[int, int]]],
                     line_len: int) -> bool:
    found_parts = 0
    first_second = [[], []]
    if position == 0:
        # check * line
        if starts_ends[line_number][0][0] == 1:
            first_second[found_parts] = starts_ends[line_number][0]
            found_parts += 1
        # check previous line
        if line_number > 0:
            if starts_ends[line_number-1][0][0] == 0 or \
            starts_ends[line_number-1][0][0] == 1:
                first_second[found_parts] = starts_ends[line_number-1][0][0]
                found_parts += 1
        # check next line
        if line_number < len(starts_ends) - 1:
            if starts_ends[line_number+1][0][0] == 0 or \
            starts_ends[line_number+1][0][0] == 1:
                first_second[found_parts] = starts_ends[line_number+1][0][0]
                found_parts += 1
    if found_parts == 2:
        return True, first_second
    if position == line_len-1:
        # check * line
        if starts_ends[line_number][-1][1] == line_len-2:
            first_second[found_parts] = starts_ends[line_number][-1]
            found_parts += 1
        # check previous line
        if line_number > 0:
            if starts_ends[line_number-1][-1][1] == line_len-1 or \
            starts_ends[line_number-1][-1][1] == line_len-2:
                first_second[found_parts] = starts_ends[line_number-1][-1]
                found_parts += 1
        # check next line
        if line_number < len(starts_ends) - 1:
            if starts_ends[line_number+1][-1][1] == line_len-1 or \
            starts_ends[line_number+1][-1][1] == line_len-2:
                first_second[found_parts] = starts_ends[line_number+1][-1]
                found_parts += 1
    if found_parts == 2:
        return True, first_second
    pass
    # part 2 - abandoned
    return False


def gear_ratios(schematic: list[str]) -> list[int]:
    width = len(schematic[0])
    all_start_ends = [get_part_numbers_in_line(schematic, i, width)
                      for i in range(len(schematic))]
    # handle the first line
    indexes = [x.start() for x in re.finditer('\*', schematic[0])]
    # ABANDONING THE 2nd part




if __name__ == "__main__":
    data = input_parsing.load_list_of_strings("../data/03-input")
    print(sum_part_numbers_in_schematic(data))
