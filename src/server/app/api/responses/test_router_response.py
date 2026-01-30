from . import BaseResponse


class TestResponse(BaseResponse):
    """Модель выходных данных для тестового ответа."""

    users_count: int
