import itertools
import re
import string
import structlog


logger = structlog.get_logger()

symbol_chars = set(s for s in string.punctuation if s != '.')
part_num_re = re.compile(r"(\d+)")


def process_part_num(y: int, x0: int, xn: int, symbols: set[tuple[int, int]]) -> int | None:
    logger.debug("Processing part number from (%d, %d]", x0, xn)
    # look at the 6+2N potential neighbors, where N is the length of the current part number
    neighbors = list(itertools.chain(
        [(y-1, i) for i in range(x0-1, xn+1)],
        [(y, x0-1), (y, xn)],
        [(y+1, i) for i in range(x0-1, xn+1)],
    ))

    logger.debug("Neighbors", n=neighbors)

    # if any neighbor is a symbol, count the part number
    return any(map(lambda n: n in symbols, neighbors))


def three_one(puzzle_input: list[str]) -> int:
    part_nums: dict[tuple[int, int, int], int] = {}
    symbols: set[tuple[int, int]] = set()

    # for each row...
    for y, line in enumerate(puzzle_input):
        # find all the part numbers
        for match in re.finditer(part_num_re, line):
            part_nums[(y, match.start(), match.end())] = int(match.group())
        # find all the symbols
        for x, char in enumerate(line):
            if char in symbol_chars:
                symbols.add((y, x))

    return sum([pn for coord, pn in part_nums.items() if process_part_num(*coord, symbols)])


def three_two(puzzle_input: list[str]) -> int:
    part_nums: dict[tuple[int, int], int] = {}
    symbols: set[tuple[int, int]] = set()
    id_gen = itertools.count()

    logger.debug("Preprocessing part numbers and symbols")
    # for each row...
    for y, line in enumerate(puzzle_input):
        # find all the part numbers
        for match in re.finditer(part_num_re, line):
            # make a unique id for each part num since one part number can span multiple 'neighbor' coords of a symbol
            pn_id = next(id_gen)
            part_nums |= { (y, xi): (pn_id, int(match.group())) for xi in range(match.start(), match.end()) }
        # locate all of the potential gears
        for x, char in enumerate(line):
            if char == "*":
                symbols.add((y, x))

    logger.debug("Checking symbols for gears", symbols=symbols)
    sum = 0
    for sy, sx in symbols:
        # 8 neighboring coords; no need to limit within schematic bounds
        neighbors = [(y, x) for y in range(sy-1, sy + 2) for x in range(sx-1, sx+2) if (y, x) in part_nums]
        logger.debug("Checking neighbors for (%d, %d)", sy, sx, neighbors=neighbors)
        # check if any neighbors are part nums; map by id but only keep the part nums
        pns = dict(part_nums[yx] for yx in neighbors).values()
        if len(pns) == 2:
            # if we found exactly 2 adjacent part numbers: it's a gear
            logger.debug("adjacent part numbers for (%d, %d)", sy, sx, part_nums=pns)
            pn1, pn2 = pns
            sum += pn1 * pn2
    return sum
        



