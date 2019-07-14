import logging

formatter = logging.Formatter(
    '[%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger = logging.getLogger('Geungjungbot')
logger.setLevel(logging.INFO)
logger.addHandler(ch)
