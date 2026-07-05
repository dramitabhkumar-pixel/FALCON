"""
==========================================================
FALCON EXCEPTIONS
==========================================================
"""


class FalconException(Exception):
    pass


class ValidationError(FalconException):
    pass


class MarketStructureError(FalconException):
    pass


class SwingError(FalconException):
    pass


class FibonacciError(FalconException):
    pass


class TradeError(FalconException):
    pass


class BrokerError(FalconException):
    pass