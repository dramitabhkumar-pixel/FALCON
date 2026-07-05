"""
==========================================================
FALCON LOGGER
==========================================================
"""

import logging
import sys


class FalconLogger:

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger is None:

            logger = logging.getLogger("FALCON")

            logger.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s : %(message)s",
                "%H:%M:%S"
            )

            console = logging.StreamHandler(sys.stdout)

            console.setFormatter(formatter)

            logger.addHandler(console)

            cls._logger = logger

        return cls._logger