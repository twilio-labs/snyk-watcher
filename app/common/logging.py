import logging

from pythonjsonlogger import jsonlogger


def getLogger(name):
    logger = logging.getLogger(name)
    json_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(sid)s %(funcName)s %(levelname)s %(asctime)s %(lineno)s %(filename)s %(name)s %(message)s')  # nopep8
    json_handler.setFormatter(formatter)
    logger.addHandler(json_handler)

    return logger
