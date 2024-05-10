import asyncio
import uuid
import random
import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from copy import deepcopy

from redis.asyncio.client import Redis

from tests.functional.settings import test_settings
from tests.functional.testdata.data import TEST_DATA, TEST_DATA_GENRE, TEST_DATA_PERSON
from tests.functional.utils.dc_objects import Response
from tests.functional.utils.films_utils import generate_films


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client() -> AsyncElasticsearch:
    es_client = AsyncElasticsearch(
        hosts=test_settings.es_host,
        verify_certs=False
    )
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='session_client', scope='session')
async def session_client() -> aiohttp.ClientSession:
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture()
def es_data(request) -> list[dict]:
    es_data = []

    index = test_settings.es_index
    type_test = request.node.get_closest_marker("fixt_data").args[0]
    # FIX: эти условия не очень хорошо, надо индекс параметром будет
    # передавать и убрать из settings es_index раз уж у нас 2 индекса
    # TODO Согласен индекс нужно передать как параметр, а в settings можно добавить все индексы или убрать
    if (type_test == 'genre' or type_test == 'limit_genre' or
            type_test == 'genre_validation' or type_test == 'redis_genre'):
        index = 'genres'
    if type_test == 'person' or type_test == 'limit_person' or type_test == 'person_validation':
        index = 'persons'
    copy_film_data = deepcopy(TEST_DATA)
    copy_genre_data = deepcopy(TEST_DATA_GENRE)
    copy_person_data = deepcopy(TEST_DATA_PERSON)
    # Генерируем данные для ES
    if type_test == 'limit':
        for _ in range(60):
            copy_film_data['id'] = str(uuid.uuid4())
            es_data.append(deepcopy(copy_film_data))

    if type_test == 'validation':
        for _ in range(3):
            copy_film_data['id'] = str(uuid.uuid4())
            es_data.append(deepcopy(copy_film_data))
        copy_film_data['id'] = str(uuid.uuid4())
        copy_film_data['imdb_rating'] = 15
        es_data.append(deepcopy(copy_film_data))
        copy_film_data['id'] = str(uuid.uuid4())
        copy_film_data['imdb_rating'] = -2
        es_data.append(deepcopy(copy_film_data))
        copy_film_data['id'] = '1123456'
        copy_film_data['imdb_rating'] = 5
        es_data.append(deepcopy(copy_film_data))

    if type_test == 'redis_search':
        for _ in range(6):
            copy_film_data['id'] = str(uuid.uuid4())
            copy_film_data['title'] = 'The Star'
            es_data.append(deepcopy(copy_film_data))

    if type_test == 'redis_genre':
        copy_genre_data = deepcopy(TEST_DATA_GENRE)
        es_data.append(deepcopy(copy_genre_data))

    if type_test == 'phrase':
        for _ in range(3):
            copy_film_data['id'] = str(uuid.uuid4())
            copy_film_data['title'] = 'The Star'
            es_data.append(deepcopy(copy_film_data))
        for _ in range(3):
            copy_film_data['id'] = str(uuid.uuid4())
            copy_film_data['title'] = 'Star Roger'
            es_data.append(deepcopy(copy_film_data))
        copy_film_data['id'] = str(uuid.uuid4())
        copy_film_data['title'] = 'Roger Philips'
        es_data.append(deepcopy(copy_film_data))

    if type_test == 'limit_genre':
        for _ in range(60):
            copy_genre_data['id'] = str(uuid.uuid4())
            copy_genre_data['name'] = f'Action{_}'
            es_data.append(deepcopy(copy_genre_data))

    if type_test == 'limit_person':
        for i in range(60):
            copy_person_data['id'] = str(uuid.uuid4())
            copy_person_data['full_name'] = f'Test_person{i}'
            es_data.append(deepcopy(copy_person_data))

    if type_test == 'genre_validation':
        for _ in range(3):
            copy_genre_data['id'] = str(uuid.uuid4())
            copy_genre_data['name'] = f'Action{_}'
            es_data.append(deepcopy(copy_genre_data))
        copy_genre_data['id'] = '123456'
        copy_genre_data['name'] = f'Action'
        es_data.append(deepcopy(copy_genre_data))

    if type_test == 'all_films':
        count = random.randint(50, 100)
        films = generate_films(count=count)
        es_data.extend(films)

    copy_film_data = deepcopy(TEST_DATA)
    if type_test == 'film':
        es_data.append(deepcopy(copy_film_data))
        for _ in range(60):
            copy_film_data['id'] = str(uuid.uuid4())
            es_data.append(deepcopy(copy_film_data))

    if type_test == 'genre':
        copy_genre_data = deepcopy(TEST_DATA_GENRE)
        es_data.append(deepcopy(copy_genre_data))
        genres = ['Melodrama', 'Sci-Fi', 'Comedy', 'Tragedy']
        for genre in genres:
            copy_genre_data['id'] = str(uuid.uuid4())
            copy_genre_data['name'] = genre
            es_data.append(deepcopy(copy_genre_data))

    if type_test == 'person':
        es_data.append(deepcopy(copy_person_data))
        persons_names = ['Ann', 'Bob', 'Ben', 'Howard']
        for name in persons_names:
            copy_person_data['id'] = str(uuid.uuid4())
            copy_person_data['full_name'] = name + ' Test'
            es_data.append(deepcopy(copy_person_data))

    if type_test == 'person_films':
        count = 15
        films = generate_films(count=count)
        es_data.extend(films)

    bulk_query: list[dict] = []
    for row in es_data:
        data = {'_index': index, '_id': row['id']}
        data.update({'_source': row})
        bulk_query.append(data)

    return bulk_query


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client: AsyncElasticsearch, redis_client: Redis, request):
    async def inner(data: list[dict], index: str) -> None:
        await redis_client.flushdb()
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)

        await es_client.indices.create(index=index)

        # refresh="wait_for" - опция для ожидания обновления индекса после выполнения async_bulk
        updated, errors = await async_bulk(client=es_client, actions=data, refresh="wait_for")

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(session_client):
    async def inner(type_api, query_data) -> Response:
        url = test_settings.service_url + '/api/v1/' + type_api + '/'
        if 'id' in query_data:
            url += query_data['id']
        get_params = {'query': query_data.get(type_api)}
        if not get_params['query']:
            get_params = None
        async with session_client.get(url, params=get_params) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        return Response(body, headers, status)

    return inner


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    client = Redis(host=test_settings.redis_host,
                   port=test_settings.redis_port,
                   decode_responses=True)
    yield client
    await client.flushdb()
    await client.close()
