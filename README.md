# logging-setup

[![PyPI](https://img.shields.io/pypi/v/loggingsetup.svg)](https://pypi.org/project/loggingsetup/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style](https://img.shields.io/badge/code%20style-PEP8-lightgrey.svg)](https://peps.python.org/pep-0008/)
[![Built on](https://img.shields.io/badge/built%20on-logging-yellow.svg)](https://docs.python.org/3/library/logging.html)

A ready-made configuration for Python's standard `logging` module.
Call `init_logging()` once, and the whole project gets colored console output, daily log files, and automatic cleanup.

## Features

- Colored console output (DEBUG white, INFO cyan, WARNING yellow, ERROR red, CRITICAL bright red)
- `STDOUT` gets messages up to WARNING, `STDERR` gets ERROR and above
- Daily log files (UTC):
  - `logs/app-YYYY-MM-DD.log` for DEBUG to WARNING
  - `logs/error-YYYY-MM-DD.log` for ERROR and CRITICAL
- Old logs are deleted automatically (default: older than 30 days), once at startup and then every day
- No need for `logging.getLogger(__name__)`: `logging.info(...)` shows the real module name (for example `app.bot`) instead of `root`
- Uncaught exceptions in the main thread and in other threads are logged as errors
- Noisy libraries (`urllib3`, `aiohttp`, `selenium`, `telethon`, `pyrogram`, `asyncio`, `apscheduler`) are limited to WARNING
- Calling `init_logging()` twice is safe: the second call is ignored

## Requirements

- Python 3.11+
- [colorama](https://pypi.org/project/colorama/)
- [APScheduler](https://pypi.org/project/APScheduler/)

## Installation

Available on [PyPI](https://pypi.org/project/loggingsetup/). See [release 0.0.2](https://pypi.org/project/loggingsetup/0.0.2/).

```bash
pip install loggingsetup
```

With [uv](https://docs.astral.sh/uv/):

```bash
uv add loggingsetup
```

> The package name is `loggingsetup`, but the import name is `logging_setup`.

## Quick start

In your main script, call it once:

```python
import logging
from logging_setup import init_logging

init_logging()

logging.info("Hello World!")
```

In every other module, just use the standard `logging`:

```python
import logging

def run():
    logging.info("Bot started")
    logging.error("Something went wrong")
```

Example output:

```
2026-10-20 09:42:16 | INFO     | app.bot | Bot started
2026-10-20 09:42:16 | ERROR    | app.bot | Something went wrong
```

> `logger = logging.getLogger(__name__)` still works if you prefer it.

## Parameters

| Parameter                 | Type   | Default  | Description                           |
|---------------------------|--------|----------|---------------------------------------|
| `directory`               | `str`  | `"logs"` | Folder for log files                  |
| `enable_console`          | `bool` | `True`   | Turn console output on or off         |
| `delete_old_logs`         | `bool` | `True`   | Turn automatic cleanup on or off      |
| `days_to_delete_old_logs` | `int`  | `30`     | Delete logs older than this many days |

```python
init_logging(directory="my_logs", enable_console=False, days_to_delete_old_logs=14)
```

## Project structure

```
logging_setup/
├── __init__.py          # exports init_logging
├── my_setup.py          # main setup function
├── formats.py           # color formatter, rotating handler, module name factory
├── filters.py           # level filters, exception hooks
└── cleanup_old_logs.py  # background cleanup of old log files
```

## Notes

- The module name is calculated from the file path relative to the current working directory. Run your project from its root folder, so `app/bot.py` is shown as `app.bot`.
- The entry script is shown as `main`, not `__main__`.
- Old files are deleted only by the cleanup job, not by `backupCount`.

## License

This project is licensed under the [MIT License](LICENSE).
