import logging

# Create logger
logger = logging.getLogger(__name__)

if not logger.handlers:
    logger.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # Handler for console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Handler for file
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)