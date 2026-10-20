import logging
from functools import lru_cache
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from colorama import Fore, Style


class ColorFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: Fore.WHITE,
        logging.INFO: Fore.CYAN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


class DatedTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rotation_filename(self, default_name):
        date_part = Path(default_name).suffix.lstrip(".")  # 2025-06-20
        base = Path(self.baseFilename)
        return str(base.with_name(f"{base.stem}-{date_part}.log"))


def install_module_name_factory(project_root: str | Path | None = None) -> None:
    """
    Replaces the logger name 'root' with the module path (like app.bot),
    so logging.info(...) works without logger = logging.getLogger(__name__).
    """
    root_dir = Path(project_root or Path.cwd()).resolve()

    @lru_cache(maxsize=None)
    def module_name(pathname: str) -> str:
        try:
            relative = Path(pathname).resolve().relative_to(root_dir)
            return ".".join(relative.with_suffix("").parts)
        except ValueError:
            return Path(pathname).stem  # file is outside the project

    old_factory = logging.getLogRecordFactory()

    def factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        if record.name == "root":
            record.name = module_name(record.pathname)
        return record

    logging.setLogRecordFactory(factory)


file_fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
date_fmt = "%Y-%m-%d %H:%M:%S"
