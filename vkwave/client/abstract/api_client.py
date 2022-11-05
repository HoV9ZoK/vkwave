from abc import ABC, abstractmethod

from vkwave.http import AbstractHTTPClient

from .context import AbstractRequestContext
from .factory import AbstractFactory
from vkwave.client.types import MethodName


class AbstractAPIClient(ABC):
    @property
    def http_client(self) -> AbstractHTTPClient:
        raise NotImplementedError("This client probably doesn't implement 'http_client' property.")

    @abstractmethod
    def set_context_factory(self, factory: AbstractFactory) -> None:
        ...

    @property
    @abstractmethod
    def context_factory(self) -> AbstractFactory:
        ...

    @abstractmethod
    def create_request(self, method_name: MethodName, params: dict) -> AbstractRequestContext:
        ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()

    @abstractmethod
    async def close(self) -> None:
        """Close resources."""
