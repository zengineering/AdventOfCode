import click
import logging
import structlog

from day_one import one_one

# Map string log levels to structlog log level numbers
log_levels = {
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50
}

commands = {
    "one": one_one
}

def get_all_input(f: click.File) -> list[str]:
    return filter(lambda x: x, map(lambda x: x.strip(), f.readlines()))

@click.command()
@click.argument("day")
@click.argument("input_file", type=click.File('r'))
@click.option("--log", type=click.Choice(logging.getLevelNamesMapping().keys()), help="Logging level")
def main(day, input_file, log):


    # Configure structlog
    if log: 
        log_level = logging.getLevelNamesMapping().get(log, logging.WARN)
    else:
        log_level = logging.INFO

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
    )

    puzzle_input = get_all_input(input_file)
    command = commands[day]
    if command is not None:
        command_output = command(puzzle_input)
        print(command_output)

main()