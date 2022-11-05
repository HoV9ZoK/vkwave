import typing

if typing.TYPE_CHECKING:
    from abstract.context import AbstractRequestContext

ErrorHandlerCallable = typing.Callable[["AbstractRequestContext"], typing.Awaitable[None]]

MethodName = typing.NewType("MethodName", str)
RequestCallbackCallable = typing.Callable[[MethodName, dict], typing.Awaitable[dict]]
SignalCallbackCallable = typing.Callable[["AbstractRequestContext"], typing.Awaitable[None]]
