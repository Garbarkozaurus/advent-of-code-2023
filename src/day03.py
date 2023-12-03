from datetime import datetime
import re
import itertools

import sys
sys.path.append("../modules/")
import input_parsing

INPUT_FILES_DIR = "../data/"


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


def extend_number(line: str, idx: int) -> str:
    before = ""
    after = ""
    for i in range(idx-1, -1, -1):
        if not line[i].isdigit():
            break
        before += line[i]
    before = before[::-1]
    for i in range(idx+1, len(line)):
        if not line[i].isdigit():
            break
        after += line[i]
    return int(f"{before}{line[idx]}{after}"), idx-len(before), idx+len(after)


def asterisk_gear_ratio(schematic: list[str], line_number: int, position: int, width: int) -> int:
    h_neighborhood = (-1, 0, 1)
    v_neighborhood = (-1, 0, 1)
    if position == 0:
        h_neighborhood = (1, 0)
    if position == width - 1:
        h_neighborhood = (0, -1)
    if line_number == 0:
        v_neighborhood = (0, 1)
    if line_number == len(schematic) - 1:
        v_neighborhood = (-1, 0)
    # [(x0, y0), (x1, y1)]
    neighborhood = list(itertools.product(h_neighborhood, v_neighborhood))
    neighborhood.remove((0, 0))
    digits_in_neighborhood = []
    for (x, y) in neighborhood:
        # being a neighbor of * guarantees for the number to be a part
        if schematic[line_number+y][position+x].isdigit():
            digits_in_neighborhood.append((x, y))
    if len(digits_in_neighborhood) < 2:
        return 0
    digits_in_neighborhood.sort(key = lambda x: x[1])  # sort by y ascending

    neighboring_numbers = []
    neighboring_positions = set()
    for (x, y) in digits_in_neighborhood:
        number, start, end = extend_number(schematic[line_number+y], position+x)
        if (line_number+y, start, end) not in neighboring_positions:
            neighboring_positions.add((line_number+y, start, end))
            neighboring_numbers.append(number)
    if len(neighboring_numbers) == 2:
        neighboring_numbers = list(neighboring_numbers)
        return neighboring_numbers[0] * neighboring_numbers[1]
    return 0


def sum_of_gear_ratios(schematic: list[str]):
    width = len(schematic[0])
    gear_ratio_sum = 0
    for i, line in enumerate(schematic):
        indices = [x.start() for x in re.finditer('\*', line)]
        for index in indices:
            gear_ratio_sum += asterisk_gear_ratio(schematic, i, index, width)
    return gear_ratio_sum


if __name__ == "__main__":
    data = input_parsing.load_list_of_strings("../data/03-input")
    print("Sum of all part numbers:", sum_part_numbers_in_schematic(data))
    print("Sum of all gear ratios:", sum_of_gear_ratios(data))
