import orjson
from fastapi import HTTPException
from pydantic import BaseModel, validator


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class BaseMixin(BaseModel):
    """
    Базовая модель
    """
    id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseFilm(BaseMixin):
    """
    Базовая модель фильма
    """
    title: str
    imdb_rating: float | None = None

    @validator('imdb_rating', pre=True, always=True)
    def validate_imdb_rating(cls, value):
        if value is not None and (value < 0 or value > 10):
            raise HTTPException(status_code=400, detail="IMDb rating must be between 0 and 10.")
        return value
