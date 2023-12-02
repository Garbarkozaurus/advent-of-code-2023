from datetime import datetime

import sys
sys.path.append("../modules/")
import input_parsing

INPUT_FILES_DIR = "../data/"


def todays_month_day(padding_target_length: int = 2) -> str:
    """Return a 0-padded number of the current day of the month.
    Used to get the number of the current date within the advent calendar"""
    return str(datetime.today().date().day).zfill(padding_target_length)


def show_to_dict(show: str) -> dict[str, int]:
    dice = show.split(',')
    dice = [num_color.split() for num_color in dice]
    show_dict = dict()
    for (number, color) in dice:
        show_dict[color] = int(number)
    if "red" not in show_dict.keys():
        show_dict["red"] = 0
    if "green" not in show_dict.keys():
        show_dict["green"] = 0
    if "blue" not in show_dict.keys():
        show_dict["blue"] = 0
    return show_dict


def parse_game(game: str) -> list[str]:
    game = game.split(": ")[1]
    shows = game.split(';')
    dict_list = [show_to_dict(show) for show in shows]
    return dict_list


def is_game_possible(game: list[dict[str, int]],
                     resource_dict: dict[str, int]) -> bool:
    for show in game:
        if show["red"] > resource_dict["red"] or \
           show["green"] > resource_dict["green"] or \
           show["blue"] > resource_dict["blue"]:
            return False
    return True


def minimum_cubes_dict(game: list[dict[str, int]]) -> dict[str, int]:
    r, g, b = [], [], []
    for show in game:
        r.append(show["red"])
        g.append(show["green"])
        b.append(show["blue"])
    min_r = max(r)
    min_g = max(g)
    min_b = max(b)
    return {"red": min_r, "green": min_g, "blue": min_b}


def dict_power(d: dict[str, int]) -> int:
    product = 1
    for value in d.values():
        product *= value
    return product


if __name__ == "__main__":
    AVAILABLE_CUBES = {"red": 12, "green": 13, "blue": 14}
    data = input_parsing.load_list_of_strings("../data/02-input")
    games = [parse_game(game) for game in data]
    valid_sum = 0
    power_sum = 0
    for i, game_dict in enumerate(games):
        if is_game_possible(game_dict, AVAILABLE_CUBES):
            valid_sum += i+1
        power_sum += dict_power(minimum_cubes_dict(game_dict))
    print("Sum of IDs of valid games:", valid_sum)
    print("Sum of power of minimal game sets:", power_sum)
