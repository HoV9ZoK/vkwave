from enum import Enum, auto


class RequestState(Enum):
    """State of request. Probably maybe useless in a lot of situtations but sometimes..."""

    NOT_SENT = auto()
    SENT = auto()


class ResultState(Enum):
    """
    State of result.
    You must check this before operating with values in (data, exception_data, exception)
    """

    NOTHING = auto()
    SUCCESS = auto()
    HANDLED_EXCEPTION = auto()
    UNHANDLED_EXCEPTION = auto()


class Signal(Enum):
    # when any exception is occurred (but after exception handlers)
    ON_EXCEPTION = auto()
    # when we are preparing to send request
    BEFORE_REQUEST = auto()
    # when we sent request and ran exception handler (if exception occurred)
    AFTER_REQUEST = auto()
