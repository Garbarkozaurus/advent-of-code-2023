DIGIT_NAMES = {"one": 1,
               "two": 2,
               "three": 3,
               "four": 4,
               "five": 5,
               "six": 6,
               "seven": 7,
               "eight": 8,
               "nine": 9}


def digit_starting_here(idx: int, s: str) -> int | None:
    if s[idx].isdigit():
        return int(s[idx])
    if s[idx:idx+3] in DIGIT_NAMES.keys():
        return DIGIT_NAMES[s[idx:idx+3]]
    if s[idx:idx+4] in DIGIT_NAMES.keys():
        return DIGIT_NAMES[s[idx:idx+4]]
    if s[idx:idx+5] in DIGIT_NAMES.keys():
        return DIGIT_NAMES[s[idx:idx+5]]


def first_and_last_digit(s: str) -> tuple[int, int]:
    first_found = False
    first_digit = 0
    last_digit = 0
    for i, _ in enumerate(s):
        d = digit_starting_here(i, s)
        if d is not None:
            last_digit = d
            if not first_found:
                first_digit = d
                first_found = True
    return first_digit, last_digit


def sum_first_and_last(s: str) -> int:
    first, last = first_and_last_digit(s)
    return 10*first+last


if __name__ == "__main__":
    with open("01-input") as fp:
        s = fp.readlines()
        s = [x.strip() for x in s]
    num_sum = sum([sum_first_and_last(x) for x in s])
    print(num_sum)
