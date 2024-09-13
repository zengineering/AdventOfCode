import click
import logging
import structlog

from day_one import one_one

# Map string log levels to structlog log level numbers
log_levels = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}

commands = {"one": one_one}


def get_all_input(f: click.File) -> list[str]:
    """
    Get puzzle input from the provided file.

    :param f: click.File from which to read input
    :returns: list of lines in the provided file
    """
    return filter(lambda x: x, map(lambda x: x.strip(), f.readlines()))


def configure_logging(preferredLevel: str | None = None, defaultLevel=logging.WARN):
    """
    Configure logging; currently structlog.

    :param preferredLevel: preferred logging level; should match one of the values from logging module
    :param defaultLevel: default logging level if preferredLevel is invalid or missing
    :returns: nothing
    """
    # Configure structlog
    if preferredLevel:
        log_level = logging.getLevelNamesMapping().get(preferredLevel, defaultLevel)
    else:
        log_level = defaultLevel

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer(),
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
def main(day, input_file, log):
    configure_logging()

    puzzle_input = get_all_input(input_file)
    command = commands[day]
    if command is not None:
        command_output = command(puzzle_input)
        print(command_output)


main()
