from dishka import Provider, Scope, provide

from ...repositories import BotUserRepository
from ...services import BotUserService


class BotServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def bot_user_service(
        self, bot_user_repository: BotUserRepository
    ) -> BotUserService:
        return BotUserService(bot_user_repository=bot_user_repository)
