import logging
import sys


def max_level_filter(max_level_name: str):
    max_level = getattr(logging, max_level_name.upper(), logging.WARNING)

    class MaxLevelFilter(logging.Filter):
        def filter(self, record):
            return record.levelno <= max_level

    return MaxLevelFilter()


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("[logging-setup] Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def handle_thread_exception(args):
    if issubclass(args.exc_type, SystemExit):
        return
    logging.error(
        "[logging-setup] Uncaught exception in thread",
        exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
    )
