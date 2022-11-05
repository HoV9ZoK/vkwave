from abc import ABC, abstractmethod
from typing import Dict, Type

from .context import AbstractRequestContext
from vkwave.client.types import MethodName, RequestCallbackCallable


class AbstractFactory(ABC):
    @abstractmethod
    def create_context(
        self,
        exceptions: Dict[Type[Exception], None],
        request_callback: RequestCallbackCallable,
        method_name: MethodName,
        request_params: dict,
        *args,
        **kwargs,
    ) -> AbstractRequestContext:
        """

        :rtype: object
        """
        ...

