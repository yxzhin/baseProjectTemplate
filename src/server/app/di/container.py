from dishka import make_async_container

from . import AppProvider

container = make_async_container(AppProvider())
