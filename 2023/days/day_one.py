import fileinput
import re
import structlog
from collections import deque

logger = structlog.get_logger()

first_num_regex = r"(\d)" # first digit in string
last_num_regex = r"(\d)(?!.*\d)" # last digit in string

# find digit or any spelled-out single-digit number
# use positive-lookahead to account for overlapping words like "twone" or "oneight"
day_two_regex = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))")

# lookup table of number { name: value }
numbers = dict(zip(
    ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine"),
    range(1, 10)
))

def get_calibration_value_day1(line: str) -> int:
    """
    Given a line of the puzzle input:
      - find the first and last numbers in the line
      - treat them as digits of a two-digit number

    Example: 
        .7....9 -> 79
        ....5.. -> 55

    :param line: single line from puzzle input
    :return: puzzle output for that line 
    """

    # extract the first digit
    m = re.search(first_num_regex, line)
    if m is not None:
        first_digit = m.group(1)
    else:
        logger.error("Unable to read first digit from input '%s'", line)
        raise ValueError("Unable to read first digit.")

    # extract the last digit
    m = re.search(last_num_regex, line)
    if m is not None:
        last_digit = m.group(1)
    else:
        logger.error("Unable to read last digit from input '%s'", line)
        raise ValueError("Unable to read last digit.")

    # convert the strings into a two-digit number of the form <first><last>
    result = int(first_digit) * 10 + int(last_digit)
    logger.debug(
        "line: %s, first: %s, last: %s, result: %d",
        line,
        first_digit,
        last_digit,
        result,
    )
    return result

def get_calibration_value_day2(line: str) -> int:
    """
    Given a line of the puzzle input:
      - find the first and last numbers in the line
      - treat them as digits of a two-digit number

    Example: 
        .7....9 -> 79
        ....5.. -> 55
        .one.2. -> 12
        .twone. -. 21

    :param line: single line from puzzle input
    :return: puzzle output for that line 
    """
    first_digit_str = None
    last_digit_str = None
    re_iter = re.finditer(day_two_regex, line)
    try:
        # extract the first number
        first_digit_str = next(re_iter).group(1)
        # extract the last number. Might throw exceptions, e.g. if there was only one number in `line`
        last_digit_str = deque(re_iter, maxlen=1).pop().group(1)
    except (StopIteration, IndexError) as e:
        logger.debug("Somewhat-expected exception while finding digits.", 
                     exc_info=e, line=line, first=first_digit_str, last=last_digit_str)

    # we should have found *something*
    if last_digit_str is None and first_digit_str is None:
        raise ValueError(f"Failed to find digits in line: {line}")
    else:
        # lookup the number by name...
        if first_digit_str in numbers:
            first_digit = numbers[first_digit_str]
        else:
            # ...or convert to int
            first_digit = int(first_digit_str)

        if last_digit_str is None:
            # if there was only one number in the string, it's the first and last 
            last_digit = first_digit
        elif last_digit_str in numbers:
            # otherwise lookup by name...
            last_digit = numbers[last_digit_str]
        else:
            # ... or convert from int
            last_digit = int(last_digit_str)

        logger.info(line, first = first_digit, last = last_digit)

        # calculate two-digit number
        return first_digit * 10 + last_digit


def one_one(puzzle_input: list[str]) -> int:
    logger.info("Day 1, part 1")
    return sum(get_calibration_value_day1(line) for line in puzzle_input)


def one_two(puzzle_input: list[str]) -> int:
    logger.info("Day 1, part 2")
    return sum(get_calibration_value_day2(line) for line in puzzle_input)
