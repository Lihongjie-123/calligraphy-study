import sys

import _load  # nopep8
import logging
from src.main.main import main

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logging.exception(ex)
        sys.exit(-1)
