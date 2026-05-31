import logging
import os

# Create logs directory if it does not exist
os.makedirs("logs", exist_ok=True)

# Create logger
logger = logging.getLogger()

if not logger.handlers:
    logger.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File output
    file_handler = logging.FileHandler(
        "logs/app.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)