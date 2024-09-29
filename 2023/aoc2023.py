import click
import logging
import structlog
from typing import Iterable

from days import one_one, one_two, two_one, two_two, three_one, three_two

commands = {
    "1.1": one_one,
    "1.2": one_two,
    "2.1": two_one,
    "2.2": two_two,
    "3.1": three_one
}


def get_all_input(f: click.File) -> Iterable[str]:
    """
    Get puzzle input from the provided file.

    :param f: click.File from which to read input
    :returns: list of lines in the provided file
    """
    return filter(lambda x: x, map(lambda x: x.strip(), f.readlines()))


def configure_logging(preferredLevel: str | None = None, defaultLevel=logging.WARN, no_color: bool = False):
    """
    Configure logging; currently structlog.

    :param preferredLevel: preferred logging level; should match one of the values from logging module
    :param defaultLevel: default logging level if preferredLevel is invalid or missing
    :returns: nothing
    """
    structlog.stdlib.recreate_defaults()

    # Configure structlog
    if preferredLevel:
        log_level = logging.getLevelNamesMapping().get(preferredLevel, defaultLevel)
    else:
        log_level = defaultLevel

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(exception_formatter=structlog.dev.rich_traceback, colors=not no_color),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
    )


@click.command()
@click.argument("day")
@click.argument("input_file", type=click.File("r"))
@click.option(
    "--log",
    type=click.Choice(logging.getLevelNamesMapping().keys()),
    help="Logging level",
)
@click.option(
    "--no-color",
    is_flag=True,
    help="Disable color in log output."
)
def main(day, input_file, log, no_color):
    configure_logging(log, no_color=no_color)
    logger = structlog.get_logger()

    command = commands[day]
    if command is not None:
        try:
            command_output = command(get_all_input(input_file))
            print(command_output)
        except Exception as e:
            logger.error("Command %s failed.", day, exc_info=True)


main()
