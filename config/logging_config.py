"""
Sky-Guard: Centralized Logging Configuration
=============================================

Production-grade logging setup with:
- Structured log formatting
- Multiple output handlers (console + file)
- Environment-aware log levels
- Performance tracking capabilities

Usage:
    from sky_guard.config.logging_config import get_logger
    logger = get_logger(__name__)
    logger.info("Operation completed", extra={'duration': 1.23})
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
import os


def setup_logging(
    log_level: str = None,
    log_file: str = None,
    console_output: bool = True
) -> None:
    """
    Configure application-wide logging.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (None = auto-generate)
        console_output: Enable console logging
    """
    
    # Determine log level from environment or default
    if log_level is None:
        log_level = os.getenv('SKYGUARD_LOG_LEVEL', 'INFO')
    
    # Create logs directory
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Generate log filename if not provided
    if log_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'skyguard_{timestamp}.log'
    else:
        log_file = Path(log_file)
    
    # Define log format
    log_format = (
        '%(asctime)s | %(levelname)-8s | %(name)s | '
        '%(funcName)s:%(lineno)d | %(message)s'
    )
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Create formatter
    formatter = logging.Formatter(log_format, datefmt=date_format)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Capture everything in file
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler (if enabled)
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        
        # Simplified format for console
        console_format = '%(levelname)-8s | %(name)s | %(message)s'
        console_formatter = logging.Formatter(console_format)
        console_handler.setFormatter(console_formatter)
        
        root_logger.addHandler(console_handler)
    
    # Log startup message
    root_logger.info('=' * 70)
    root_logger.info('Sky-Guard Logging System Initialized')
    root_logger.info(f'Log Level: {log_level}')
    root_logger.info(f'Log File: {log_file}')
    root_logger.info('=' * 70)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started", extra={'records': 1000})
    """
    return logging.getLogger(name)


class LoggerMixin:
    """
    Mixin class to add logging capability to any class.
    
    Usage:
        class MyDataProcessor(LoggerMixin):
            def process(self):
                self.logger.info("Processing data")
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger


# Initialize logging on module import
# This ensures logging is configured before any other module uses it
if not logging.getLogger().handlers:
    setup_logging()