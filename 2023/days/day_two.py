import re
import structlog
from dataclasses import dataclass
from collections import defaultdict
from typing import Iterable

logger = structlog.get_logger()

@dataclass
class Game:
    index: int
    blue: int
    red: int
    green: int

    def is_possible(self, max_red: int, max_green: int, max_blue: int) -> bool:
        return self.red <= max_red and self.green <= max_green and self.blue <= max_blue
    
    def power(self) -> int:
        return self.blue * self.red * self.green


def parse_game(line: str):
    game_re = re.compile(r"Game\s+(\d+):\s+(.*)")
    cube_re = re.compile(r"(\d+)\s+(\w+)")

    m = re.search(game_re, line)
    if m is None:
        logger.error("Failed to parse game", line=line)
    game, content = m.groups()

    max_counts = defaultdict(int)
    for cubeset in content.split(";"):
        for color_count in cubeset.split(","):
            try:
                m = re.search(cube_re, color_count)
                if m is None:
                    logger.error("Failed to parse color count", game=game, color_count=color_count)
                else:
                    (count_str, color) = m.groups()
                    count = int(count_str)
                    if max_counts[color] < count:
                        max_counts[color] = count
            except Exception:
                logger.exception("Unexpected error during parsing.", exc_info=True, line=line)

    return Game(int(game), max_counts["blue"], max_counts["red"], max_counts["green"])
        

def two_one(puzzle_input: Iterable[str]) -> int:
    games = (parse_game(line) for line in puzzle_input)
    return sum((g.index for g in games if g.is_possible(12, 13, 14)))

def two_two(puzzle_input: Iterable[str]) -> int:
    games = (parse_game(line) for line in puzzle_input)
    return sum((g.power() for g in games))
