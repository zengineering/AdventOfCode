import itertools
import re
import string
import structlog
from collections import defaultdict
from typing import Iterable


logger = structlog.get_logger()

digits = set(string.digits)
symbols = set(s for s in string.punctuation if s != '.')
part_num_re = re.compile(r"(\d+)")

def save_input(puzzle_input: Iterable[str]) -> list[str]:
    return [line for line in puzzle_input]

def check_bounds(y, x, y_max, x_max):
    return x >= 0 and x < x_max and y >= 0 and y < y_max

def process_part_num(y: int, x0: int, xn: int, schematic: list[list[str]]) -> int | None:
    logger.debug("Processing part number from (%d, %d]", x0, xn)
    # look at the 6+2N potential neighbors, where N is the length of the current part number
    potential_neighbors = list(itertools.chain(
        [(y-1, i) for i in range(x0-1, xn+1)],
        [(y, x0-1), (y, xn)],
        [(y+1, i) for i in range(x0-1, xn+1)],
    ))

    logger.debug("Potential neighbors", n=potential_neighbors)

    # limit the neighbors to legitimate coordinates (i.e. not falling off the end of a row/col)
    neighbors = [pn for pn in potential_neighbors if check_bounds(pn[0], pn[1], len(schematic), len(schematic[y]))]

    logger.debug("Legit neighbors", n=neighbors)
    logger.debug("Neighbors:", n="".join(schematic[y][x] for y, x in neighbors))

    # if any neighbor is a symbol, count the part number
    return any(map(lambda y_x: schematic[y_x[0]][y_x[1]] in symbols, neighbors))


def three_one(puzzle_input: list[str]) -> int:
    part_nums: dict[tuple[int, int, int], int] = {}

    # for each row...
    for y, line in enumerate(puzzle_input):
        # find all the part numbers
        for match in re.finditer(part_num_re, line):
            part_nums[(y, match.start(), match.end())] = int(match.group())

    return sum([pn for coord, pn in part_nums.items() if process_part_num(*coord, puzzle_input)])



def three_two(puzzle_input: list[str]) -> int:
    part_nums_edges: dict[tuple[int, int], int] = {}
    symbols: dict[tuple[int, int], int] = {}
    schematic = save_input(puzzle_input)

    # for each row...
    for y, line in enumerate(schematic):
        # find all the part numbers
        for match in re.finditer(part_num_re, line):
            for yi in range(y-1, y+2):
                for xi in range(match.start(), match.end()):
                    part_nums_edges[(yi, xi)] = int(match.group())
        # and find all fo the symbols
        for x, char in enumerate(range(len(line))):
            symbols[(y, x)] = char

    return sum(part_nums.get(coord, 0) for coord in symbols.keys())
    for coord in symbols.keys():
        pass


