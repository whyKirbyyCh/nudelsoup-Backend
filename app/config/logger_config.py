import sys
from loguru import logger as loguru_logger


class Logger:
    """Class to configure the Loguru logger with custom settings."""

    _instance = None

    def __new__(cls, *args, **kwargs) -> "Logger":
        """Create a singleton instance of Logger."""
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_level: str = "INFO") -> None:
        """Initialize the Logger with the default log level."""
        if not getattr(self, '_configured', False):
            self.log_level: str = log_level
            self._configure_logger()
            self._configured = True

    def _configure_logger(self) -> None:
        """
        Configure the global Loguru logger with specified settings.

        Args:
            self

        Returns:
            None

        Raises:
            None

        """
        loguru_logger.remove()

        self.log = loguru_logger

        self.log.add(
            sys.stdout,
            format="<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | <cyan>{name}</cyan> | "
                   "<level>{level}</level> | <white>{message}</white>",
            level=self.log_level,
            colorize=True,
        )

    @classmethod
    def get_logger(cls) -> loguru_logger:
        """Get the configured logger instance.

        Args:
            cls

        Returns:
            logger: The configured Loguru logger.

        Raises:
            None
        """
        if not cls._instance:
            cls()
        return cls._instance.log
