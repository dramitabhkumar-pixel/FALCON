"""
=========================================================
Project FALCON
Base Engine
Version : 1.0
=========================================================
"""

from abc import ABC, abstractmethod


class BaseEngine(ABC):
    """
    Base class for all FALCON engines.

    Every engine should inherit from this class.
    """

    def __init__(self, name: str):

        self.name = name

    def log(self, message: str) -> None:
        """
        Simple logger.
        """

        print(f"[{self.name}] {message}")

    @abstractmethod
    def validate(self, data):
        """
        Validate input data.
        """

        pass

    @abstractmethod
    def run(self, data):
        """
        Execute engine.
        """

        pass