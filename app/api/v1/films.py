from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from app.services.film import FilmService, get_film_service
from app.utils.dc_objects import PaginatedParams
from pydantic import BaseModel
from typing import List
from uuid import UUID

router = APIRouter()


class BaseFilmModelResponse(BaseModel):
    """
    Базовая модель фильма для ответа API
    """
    uuid: UUID
    title: str
    imdb_rating: float


class BasePersonModelResponse(BaseModel):
    """
    Базовая модель персоны для ответа API
    """
    uuid: UUID
    full_name: str


class GenreResponse(BaseModel):
    """
    Базовая модель для жанров ответа API
    """
    uuid: UUID
    name: str


class DirectorResponse(BasePersonModelResponse):
    """
    Модель режиссёра для ответа API
    """
    pass


class ActorResponse(BasePersonModelResponse):
    """
    Модель актера для ответа API
    """
    pass


class WriterResponse(BasePersonModelResponse):
    """
    Модель сценариста для ответа API
    """
    pass


class FilmResponse(BaseFilmModelResponse):
    """
    Модель фильма ответа API
    """
    description: str | None = None
    genre: List[GenreResponse]
    directors: List[DirectorResponse]
    actors: List[ActorResponse]
    writers: List[WriterResponse]


class FilmListResponse(BaseFilmModelResponse):
    """
    Модель для списка фильмов ответа API
    """
    pass


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get('/{film_id}', response_model=FilmResponse)
async def film_details(
        film_id: UUID = Path(..., description='film id'),
        film_service: FilmService = Depends(get_film_service)
) -> FilmResponse:
    """
    Получить информацию о фильме

    - **film_id**: идентификатор фильма
    """
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='film not found')

    # Преобразование данных об актёрах, сценаристах, режиссерах
    actors_response = [
        ActorResponse(uuid=actor.id, full_name=actor.name) for actor in film.actors
    ]
    writers_response = [
        WriterResponse(uuid=writer.id, full_name=writer.name) for writer in film.writers
    ]
    directors_response = [
        DirectorResponse(
            uuid=director.uuid,
            full_name=director.full_name
        ) for director in film.director
    ]
    genre_response = [
        GenreResponse(name=genre.name, uuid=genre.uuid) for genre in film.genre
    ]

    # Создание и возврат объекта ответа, используя преобразованные данные
    return FilmResponse(
        uuid=film.id,
        title=film.title,
        description=film.description,
        imdb_rating=film.imdb_rating,
        genre=genre_response,
        directors=directors_response,
        actors_names=film.actors_names,
        writers_names=film.writers_names,
        actors=actors_response,
        writers=writers_response
    )


@router.get(
    '/',
    response_model=List[FilmListResponse],
)
async def list_films(
        sort: str | None = '-imdb_rating',
        genre: str | None = Query(None, description='Filter by genre'),
        page_size: int = PaginatedParams.page_size,
        page_number: int = PaginatedParams.page_number,
        film_service: FilmService = Depends(get_film_service)) -> List[FilmListResponse]:
    """
    Получить список фильмов"

    - **sort**: сортировка по рейтингу (по убыванию)
    - **genre**: фильтрация по жанру
    - **page_size**: размер страницы
    - **page_number**: номер страницы
    """
    films = await film_service.get_films(
        sort=sort, genre=genre, page_size=page_size, page_number=page_number)
    return [FilmListResponse(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating) for film in films]


@router.get('/search/', response_model=List[FilmListResponse])
async def search_films(
        query: str = Query(..., description='Search query'),
        page_size: int = PaginatedParams.page_size,
        page_number: int = PaginatedParams.page_number,
        film_service: FilmService =
        Depends(get_film_service)) -> List[FilmListResponse]:
    """
    Поиск фильмов по запросу

    - **query**: запрос поиска
    - **page_size**: размер страницы
    - **page_number**: номер страницы

    """
    films = await film_service.search_films(
        query=query, page_size=page_size, page_number=page_number)

    return [FilmListResponse(
        uuid=film.id, title=film.title, imdb_rating=film.imdb_rating
    ) for film in films]
