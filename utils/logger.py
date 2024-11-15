# utils/logger.py
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='app.log',
        filemode='w',
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    )
