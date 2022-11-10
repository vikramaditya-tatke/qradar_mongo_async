import logging


def init_logging():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        filename="pymongo.log",
        filemode="w",
    )  # pass explicit filename here
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # add the handler to the root logger
    logging.getLogger().addHandler(console)
    logger = logging.getLogger()  # get the root logger
    logger.warning("This should go in the file.")
