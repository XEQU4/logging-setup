"""
Initializes the application's logging system.

Features:
- Automatically creates a `logs/` directory if it doesn't exist.
- Logs messages from DEBUG up to WARNING into `logs/app-YYYY-MM-DD.log`.
- Logs all ERROR and CRITICAL messages into `logs/error-YYYY-MM-DD.log`.
- Creates a new log file every day (daily rotation by date, UTC).
- Colored console output:
    - DEBUG — white
    - INFO — cyan
    - WARNING — yellow
    - ERROR — red
    - CRITICAL — bright red
- STDOUT receives messages up to WARNING, STDERR receives ERROR and above.
- Works without `logging.getLogger(__name__)`: records sent through the root
  logger (`logging.info(...)`) get the module name (e.g. `app.bot`) instead of `root`.
- All uncaught exceptions (`sys.excepthook`) and uncaught exceptions in threads
  (`threading.excepthook`) are logged as ERRORs.
- Noisy third-party loggers (urllib3, aiohttp, selenium, telethon, pyrogram,
  asyncio, apscheduler) are limited to WARNING.
- Old log files older than 30 days are deleted in the background:
  once at startup and then every day (`APScheduler`, background scheduler).
- Repeated calls of `init_logging()` are ignored.

Example of generated log files:
- logs/app-2025-06-20.log
- logs/error-2025-06-20.log

Usage:
- Call once in the main entry script:
      from logging_setup import init_logging
      init_logging()
- In all other modules just use:
      import logging
      logging.info("message")
  (`logger = logging.getLogger(__name__)` still works, but is optional.)

Note:
- The module name is calculated from the file path relative to the current
  working directory. If the project is started from another folder, pass the
  path to `install_module_name_factory(...)`.
- The entry script is shown as `main`, not `__main__`.
- The system is modular and extensible via `filters.py`, `formats.py`, `cleanup_old_logs.py`.
"""
from .my_setup import init_logging

__all__ = [
    'init_logging',
]
