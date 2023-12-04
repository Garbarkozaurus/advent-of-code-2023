from datetime import datetime

import sys
sys.path.append("../modules/")
import input_parsing

INPUT_FILES_DIR = "../data/"


def todays_month_day(padding_target_length: int = 2) -> str:
    """Return a 0-padded number of the current day of the month.
    Used to get the number of the current date within the advent calendar"""
    return str(datetime.today().date().day).zfill(padding_target_length)


def parse_card(line: str) -> tuple[list[int], list[int]]:
    all_numbers = line.split(": ")[1]
    winning, card = all_numbers.split('|')
    winning = [x.strip() for x in winning.split()]
    card = [x.strip() for x in card.split()]
    winning = list(map(int, winning))
    card = list(map(int, card))
    return winning, card


def winning_cards(line: str) -> set[int]:
    winning, card = parse_card(line)
    return set([n for n in card if n in winning])


def card_points(line: str) -> int:
    winners = winning_cards(line)
    n = len(winners)
    if n > 0:
        return 2 ** (n - 1)
    return 0


def new_cards(line: str, card_number: int) -> list[int]:
    winning, card = parse_card(line)
    n = len(winning)
    return [card_number+i+1 for i in range(n)]


#
def count_scratchcards(card_pile: list[str]):
    print(card_pile[0])
    print(new_cards(card_pile[0], 0))


if __name__ == "__main__":
    data = input_parsing.load_list_of_strings(f"{INPUT_FILES_DIR}{todays_month_day(2)}-input")
    print("Sum of card points:", sum([card_points(line) for line in data]))
    count_scratchcards(data)