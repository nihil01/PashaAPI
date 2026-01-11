import logging.handlers
import time

def setup_api_logger(api_type: str):
    handler = logging.handlers.WatchedFileHandler(f"{api_type}.log")
    formatter = logging.Formatter(
        f'%(asctime)s {api_type} [%(process)d]: %(message)s',
        '%b %d %H:%M:%S')


    formatter.converter = time.localtime
    handler.setFormatter(formatter)


    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
