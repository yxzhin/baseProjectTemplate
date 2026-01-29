from pydantic import BaseModel


class GeneralMessageResponse(BaseModel):
    """Модель выходных данных для общего ответа с сообщением."""

    message: str
