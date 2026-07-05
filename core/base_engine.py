"""
==========================================================
FALCON BASE ENGINE
==========================================================
"""

from abc import ABC

from core.logger import FalconLogger


class BaseEngine(ABC):

    def __init__(self):

        self.logger = FalconLogger.get_logger()

    def log(self, message):

        self.logger.info(message)

    def reset(self):

        pass

    def validate(self):

        return True