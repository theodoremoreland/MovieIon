import logging
import logging.handlers as handlers

logger = logging.getLogger("movie-ion")
fileHandler = handlers.RotatingFileHandler(
    "movie-ion.log", maxBytes=5000, backupCount=2
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.setLevel(
    logging.DEBUG
)  # This needs to be set. logger.error(), logger.debug(), etc. will not work without this.
