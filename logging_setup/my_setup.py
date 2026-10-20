import logging
import os
import sys
import threading
from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from colorama import init

from logging_setup.cleanup_old_logs import cleanup_old_logs_by_filename
from logging_setup.filters import max_level_filter, handle_exception, handle_thread_exception
from logging_setup.formats import ColorFormatter, file_fmt, date_fmt, DatedTimedRotatingFileHandler, \
    install_module_name_factory

_initialized = False

NOISY_LOGGERS = (
    "urllib3", "aiohttp", "selenium", "telethon",
    "pyrogram", "asyncio", "apscheduler",
)


def init_logging(
        directory: str = "logs",
        enable_console: bool = True,
        delete_old_logs: bool = True,
        days_to_delete_old_logs: int = 30,
):
    """
    Initialization of logging of the entire project and configuration.

    :param directory: The directory where the logs (app/error) from the root of the project will be stored.
    :param enable_console: Enable or Disable logging to the console.
    :param delete_old_logs: Delete or Not Delete old logs.
    :param days_to_delete_old_logs: Delete logs older than these days.
    """
    global _initialized
    if _initialized:
        return
    _initialized = True

    # Automatically reset the color
    init(autoreset=True)

    os.makedirs(directory, exist_ok=True)

    color_formatter = ColorFormatter(fmt=file_fmt, datefmt=date_fmt)
    file_formatter = logging.Formatter(fmt=file_fmt, datefmt=date_fmt)
    handlers: list[logging.Handler] = []

    # Console handlers
    if enable_console:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(color_formatter)
        stdout_handler.addFilter(max_level_filter("WARNING"))

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)
        stderr_handler.setFormatter(color_formatter)

        handlers.extend((stdout_handler, stderr_handler))

    # File handlers with date rotation
    # backupCount=0: old files are deleted only by cleanup_old_logs_by_filename
    rotating_file = DatedTimedRotatingFileHandler(
        filename=f"{directory}/app.log",
        when="midnight",
        interval=1,
        backupCount=0,
        encoding="utf-8",
        utc=True,
    )
    rotating_file.setLevel(logging.DEBUG)
    rotating_file.setFormatter(file_formatter)
    rotating_file.addFilter(max_level_filter("WARNING"))

    rotating_error = DatedTimedRotatingFileHandler(
        filename=f"{directory}/error.log",
        when="midnight",
        interval=1,
        backupCount=0,
        encoding="utf-8",
        utc=True,
    )
    rotating_error.setLevel(logging.ERROR)
    rotating_error.setFormatter(file_formatter)

    handlers.extend((rotating_file, rotating_error))

    # Replace logger name "root" with the module name
    install_module_name_factory()

    # Root logger (force=True replaces handlers that were set before)
    logging.basicConfig(level=logging.DEBUG, handlers=handlers, force=True)

    # Make noisy libraries quiet
    for name in NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

    # Global error interception
    sys.excepthook = handle_exception
    threading.excepthook = handle_thread_exception

    # Background cleanup of old logs
    scheduler = BackgroundScheduler()
    scheduler.start()

    scheduler.add_job(
        cleanup_old_logs_by_filename,
        IntervalTrigger(days=1),
        id="cleanup_old_logs",
        replace_existing=True,
        next_run_time=datetime.now(timezone.utc),
        kwargs={
            "delete_old_logs": delete_old_logs,
            "days": days_to_delete_old_logs,
            "logs_dir": directory,
        },
    )
