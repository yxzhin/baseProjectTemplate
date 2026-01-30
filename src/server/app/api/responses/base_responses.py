from pydantic import BaseModel


class BaseResponse(BaseModel):
    """Модель выходных данных для общего ответа с сообщением."""

    success: bool
    message: str
