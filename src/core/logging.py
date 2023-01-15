import logging

# Central log format for root logger
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def setup_root_logger():
    """ Setup configuration of the root logger of the application """

    # Get instance of root logger
    logger = logging.getLogger('')

    # Configure handler, formatter and level
    console = logging.StreamHandler()
    formatter = logging.Formatter(LOG_FORMAT)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.setLevel(logging.INFO)
