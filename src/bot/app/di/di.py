import inspect
from contextvars import ContextVar
from functools import wraps
from typing import get_type_hints

from discord import Interaction
from dishka import AsyncContainer, Scope, make_async_container

from ..http import APIClient
from .providers import (
    APIClientFactoryProvider,
    BotRepositoryProvider,
    BotServiceProvider,
)


def create_bot_container(api_client_factory: type[APIClient]):
    return make_async_container(
        BotServiceProvider(),
        BotRepositoryProvider(),
        APIClientFactoryProvider(api_client_factory=api_client_factory),
    )


def with_di(handler):
    @wraps(handler)
    async def wrapper(self, interaction: Interaction, *args, **kwargs):
        container = self.bot.container

        async with container(
            scope=Scope.REQUEST,
            context={Interaction: interaction},
        ) as request_container:
            token = request_container_var.set(request_container)
            try:
                return await handler(self, interaction, *args, **kwargs)
            finally:
                request_container_var.reset(token)

    return wrapper


request_container_var: ContextVar[AsyncContainer] = ContextVar("request_container")


def inject(func):
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        bound = sig.bind_partial(*args, **kwargs)

        missing = [
            name
            for name, param in sig.parameters.items()
            if name not in bound.arguments and name in type_hints
        ]

        if not missing:
            return await func(*bound.args, **bound.kwargs)

        container = request_container_var.get()

        for name in missing:
            dep_type = type_hints[name]

            value = await container.get(dep_type)
            bound.arguments[name] = value

        return await func(*bound.args, **bound.kwargs)

    return wrapper
