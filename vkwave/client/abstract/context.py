import typing
from abc import ABC, abstractmethod

from vkwave.client.enums import Signal, ResultState
from ..types import ErrorHandlerCallable, SignalCallbackCallable


class AbstractRequestContext(ABC):
    """
    Context of request. It is being returned from `create_request` function.
    Needed to work with request specified things.
    """

    @property
    @abstractmethod
    def result(self) -> "AbstractResultContext":
        ...

    @abstractmethod
    def signal(self, signal: Signal, callback: SignalCallbackCallable) -> None:
        ...

    @abstractmethod
    def set_exception_handler(
        self,
        exception: typing.Type[Exception],
        handler: ErrorHandlerCallable,
    ) -> None:
        ...

    @abstractmethod
    async def send_request(self) -> None:
        ...


class AbstractResultContext(ABC):
    @property
    @abstractmethod
    def state(self) -> "ResultState":
        """Здесь должно быть описание..."""
        ...

    @state.setter
    @abstractmethod
    def state(self, state: ResultState) -> None:
        ...

    @property
    @abstractmethod
    def exception(self) -> typing.Optional[Exception]:
        """Exception raised during calling `request_callback`"""
        ...

    @exception.setter
    @abstractmethod
    def exception(self, exception: Exception) -> None:
        ...

    @property
    @abstractmethod
    def exception_data(self) -> typing.Optional[dict]:
        """Data is set by exception handler."""
        ...

    @exception_data.setter
    @abstractmethod
    def exception_data(self, exception_data: dict) -> None:
        ...

    @property
    @abstractmethod
    def data(self) -> typing.Optional[dict]:
        """Result of `request_callback`."""
        ...

    @data.setter
    @abstractmethod
    def data(self, data: dict) -> None:
        ...
