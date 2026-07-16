"""Application entry point for ClipTranslate."""

import logging
import logging.handlers
import sys
from pathlib import Path

from config import _runtime_dir


def _setup_logging() -> None:
    """Configure rotating logging to file and console."""
    if getattr(_setup_logging, "_done", False):
        return

    log_dir = _runtime_dir() / "resource"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    def _log_unhandled_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger().exception(
            "Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = _log_unhandled_exception
    _setup_logging._done = True


def main() -> None:
    """Run the ClipTranslate application."""
    _setup_logging()

    from app_ui import ClipTranslateApp

    app = ClipTranslateApp()
    app.run()


if __name__ == "__main__":
    main()
