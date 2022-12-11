import typing

from vkwave.client.enums import RequestState, ResultState, Signal

from typing_extensions import final

from vkwave.client.types import (
    ErrorHandlerCallable,
    MethodName,
    RequestCallbackCallable,
    SignalCallbackCallable,
)

from vkwave.client.abstract.context import AbstractResultContext, AbstractRequestContext


async def _noop_error_handler(ctx: "DefaultRequestContext") -> None:
    """This handler does nothing. You should replace that."""


class DefaultRequestContext(AbstractRequestContext):
    """
    Context of request. It is being returned from `create_request` function.
    Needed to work with request specified things.
    """
    def __init__(
        self,
        request_callback: RequestCallbackCallable,
        method_name: MethodName,
        request_params: dict,
        exceptions: typing.Optional[typing.Dict[typing.Type[Exception], None]] = None,
    ):
        """
        :param request_callback: callable thing that will be called on `ctx.send_request`.
        :param method_name: name of method
        :param request_params: request params
        :param exceptions: possible exceptions while calling `request_callback`.
         There are should be only client specified exceptions.

        """
        self.state: RequestState = RequestState.NOT_SENT

        self.request_callback = request_callback
        self.request_params = request_params
        self.method_name = method_name
        self._result = DefaultResultContext()

        self._signals: typing.Dict[Signal, typing.List[SignalCallbackCallable]] = {
            Signal.ON_EXCEPTION: [],
            Signal.BEFORE_REQUEST: [],
            Signal.AFTER_REQUEST: [],
        }

        self._exception_handlers: typing.Dict[typing.Type[Exception], ErrorHandlerCallable] = {}

        if exceptions is None:
            exceptions = {}

        # set default handlers
        for exception in exceptions:
            self._exception_handlers[exception] = _noop_error_handler

    @property
    def result(self) -> "AbstractResultContext":
        return self._result

    @final
    async def _handle_exception(self, exception: Exception) -> bool:
        handler = self._exception_handlers.get(type(exception))
        if handler and handler is not _noop_error_handler:
            await handler(self)
            return True
        return False

    def signal(self, signal: Signal, callback: SignalCallbackCallable) -> None:
        self._signals[signal].append(callback)

    async def _push_signal(self, signal: Signal) -> None:
        for callback in self._signals[signal]:
            await callback(self)

    def set_exception_handler(
        self,
        exception: typing.Type[Exception],
        handler: ErrorHandlerCallable,
    ) -> None:
        if not self._exception_handlers.get(exception):
            raise ValueError("Unallowed exception")
        self._exception_handlers[exception] = handler

    @final
    async def send_request(self) -> None:
        await self._push_signal(Signal.BEFORE_REQUEST)

        try:
            result = await self.request_callback(self.method_name, self.request_params)
            self._result.state = ResultState.SUCCESS
            self._result.data = result
        except Exception as exc:
            self._result.exception = exc
            if await self._handle_exception(exc):
                self._result._state = ResultState.HANDLED_EXCEPTION
            else:
                self._result._state = ResultState.UNHANDLED_EXCEPTION
            await self._push_signal(Signal.ON_EXCEPTION)

        self.state = RequestState.SENT
        await self._push_signal(Signal.AFTER_REQUEST)


class DefaultResultContext(AbstractResultContext):
    def __init__(self):
        self._state: ResultState = ResultState.NOTHING
        self._exception: typing.Optional[Exception] = None
        self._exception_data: typing.Optional[dict] = None
        self._data: typing.Optional[dict] = None

    @property
    def state(self) -> "ResultState":
        return self._state

    @state.setter
    def state(self, value: ResultState):
        self._state = value

    @property
    def exception(self) -> typing.Optional[Exception]:
        """Exception raised during calling `request_callback`"""
        return self._exception

    @exception.setter
    def exception(self, value: Exception) -> None:
        self._exception = value

    @property
    def exception_data(self) -> typing.Optional[dict]:
        """Data is set by exception handler."""
        return self._exception_data

    @exception_data.setter
    def exception_data(self, value: dict) -> None:
        self._exception_data = value

    @property
    def data(self) -> typing.Optional[dict]:
        """Result of `request_callback`."""
        return self._data

    @data.setter
    def data(self, value: dict) -> None:
        self._data = value
