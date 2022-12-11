from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Type, TypeVar, Union

from vkwave.bots.core.dispatching.events.base import BaseEvent
from vkwave.bots.core.types.bot_type import BotType
from vkwave.types.bot_events import BotEventType
from vkwave.types.user_events import EventId, get_EventId_by_id

AnyEventType = TypeVar('AnyEventType')


class BaseResultCaster(ABC):
    @abstractmethod
    async def cast(self, result: Any, event: BaseEvent):
        ...


class ResultCaster(BaseResultCaster):
    def __init__(self):
        self.handlers: Dict[Tuple[Union[BotEventType, EventId, AnyEventType], Type[Any]],
                            Callable[[Tuple[Type[Any], BaseEvent]], Awaitable[None]]] = {}

        self.add_caster(str, _default_str_handler, BotEventType.MESSAGE_NEW, EventId.MESSAGE_EVENT)
        self.add_caster(type(None), _default_none_handler, AnyEventType)

    def add_caster(
        self,
        typeof: Type[Any],
        handler: Callable[[Tuple[Type[Any], BaseEvent]], Awaitable[None]],
        *event_type: Union[BotEventType, EventId, AnyEventType],
    ):
        for et in event_type:
            self.handlers[(et, typeof)] = handler

    def remove_caster(
        self,
        typeof: Type[Any],
        *event_type: Union[BotEventType, EventId, AnyEventType],
    ):
        for et in event_type:
            self.handlers.pop((et, typeof), None)

    async def cast(self, result: Any, event: BaseEvent):
        typeof = type(result)

        handler: Optional[Callable[[Tuple[Type[Any], BaseEvent]], Awaitable[None]]] = \
            self.handlers.get((AnyEventType, typeof), None)

        # Логично, что AnyEventType покроет BotEventType | EventId, поэтому его первым
        if handler is None:
            event_type: Union[BotEventType, EventId] = BotEventType[event.object.type.upper()] \
                if event.bot_type is BotType.BOT else \
                get_EventId_by_id(event.object.object.event_id)
            handler = self.handlers.get((event_type, typeof), None)

        if handler is not None:
            await handler(result, event)


async def _default_none_handler(some, event: BaseEvent):
    pass


async def _default_str_handler(some: str, event: BaseEvent):
    peer_id = event.object.object.peer_id if event.bot_type is BotType.USER else event.object.object.message.peer_id
    await event.api_ctx.messages.send(random_id=0, peer_id=peer_id, message=some)
