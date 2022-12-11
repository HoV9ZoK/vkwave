"""
Factory of context.
"""
from typing import Dict, Type
#
from .context import DefaultRequestContext
from vkwave.client.types import MethodName, RequestCallbackCallable

from vkwave.client.abstract.factory import AbstractFactory


class DefaultFactory(AbstractFactory):
    def create_context(
        self,
        exceptions: Dict[Type[Exception], None],
        request_callback: RequestCallbackCallable,
        method_name: MethodName,
        request_params: dict,
        *args,
        **kwargs,
    ) -> DefaultRequestContext:
        return DefaultRequestContext(
            exceptions=exceptions,
            request_callback=request_callback,
            method_name=method_name,
            request_params=request_params,
        )
