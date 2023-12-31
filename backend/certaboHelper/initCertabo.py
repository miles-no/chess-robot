import sys
import logging
import logging.handlers
import os
import importlib.util
from certaboHelper.certabo import CERTABO_DATA_PATH

def InitializeCertabo():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

    filehandler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(CERTABO_DATA_PATH, "certabo-lichess.log"), backupCount=12
    )
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    logging.info("certabo-lichess.py startup")

    simplejson_spec = importlib.util.find_spec("simplejson")
    if simplejson_spec is not None:
        print(f'ERROR: simplejson is installed. The berserk lichess client will not work with simplejson. Please remove the module. Aborting.')
        sys.exit(-1)

