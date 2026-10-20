import logging

from datetime import datetime, timedelta, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


def cleanup_old_logs_by_filename(
        logs_dir: str = "logs",
        days: int = 30,
        delete_old_logs: bool = True
) -> None:
    """
    The function for deleting old logging files is automatic.

    :param logs_dir: The directory where the logs are stored, from where they will be deleted.
    :param days: Deleting logs that are older than the specified days.
    :param delete_old_logs: A bullseye value, if True, it deletes the old logs.
    """
    if not delete_old_logs:
        return

    cutoff = datetime.now(timezone.utc).date() - timedelta(days=days)
    deleted_files = 0

    for file in Path(logs_dir).glob("*-????-??-??.log"):
        try:
            file_date = datetime.strptime(file.stem[-10:], "%Y-%m-%d").date()
            if file_date < cutoff:
                file.unlink()
                deleted_files += 1
                logger.info(f"[logging-setup] The log was deleted: {file.name}")
        except Exception as e:
            logger.warning(f"[logging-setup] File problem {file.name}: {e}")

    logger.info(f"[logging-setup] Deleted {deleted_files} logs older than {days} days.")
