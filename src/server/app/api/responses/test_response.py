from pydantic import BaseModel


class TestResponse(BaseModel):
    """Модель выходных данных для тестового ответа."""

    message: str
    users_count: int
