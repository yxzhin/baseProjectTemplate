from dishka import Provider, Scope, provide

from ...http import APIClient
from ...repositories import BotUserRepository


class BotRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def bot_user_repo(self, api_client_factory: type[APIClient]) -> BotUserRepository:
        return BotUserRepository(api_client_factory=api_client_factory)
