import logging

def logger_config():
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    return logger