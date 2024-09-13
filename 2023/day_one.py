import fileinput
import re
import structlog

logger = structlog.get_logger()

first_num_regex = r"(\d)"
last_num_regex = r"(\d)(?!.*\d)"

def get_calibration_value(line: str) -> int:
    m = re.search(first_num_regex, line)
    if m is not None:
        first_digit = m.group(1)
    else:
        logger.error("Unable to read first digit from input '%s'", line)
        raise ValueError("Unable to read first digit.")

    m = re.search(last_num_regex, line)
    if m is not None:
        last_digit = m.group(1)
    else:
        logger.error("Unable to read last digit from input '%s'", line)
        raise ValueError("Unable to read last digit.")

    result = int(first_digit) * 10 + int(last_digit)
    logger.debug("line: %s, first: %s, last: %s, result: %d", line, first_digit, last_digit, result)
    return result


def one_one(puzzle_input: list[str]) -> int:
    logger.info("Day 1, part 1")
    return sum(get_calibration_value(line) for line in puzzle_input)


if __name__ == "__main__":
    one()