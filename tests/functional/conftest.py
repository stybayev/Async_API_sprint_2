import asyncio
import sys
import uuid
from copy import deepcopy

import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from tests.functional.settings import test_settings
from tests.functional.testdata.data import TEST_DATA
from tests.functional.utils.dc_objects import Response


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
    type_test = request.node.get_closest_marker("fixt_data").args[0]
    # Генерируем данные для ES
    if type_test == 'limit':
        for _ in range(60):
            TEST_DATA['id'] = str(uuid.uuid4())
            es_data.append(deepcopy(TEST_DATA))

    if type_test == 'validation':
        for _ in range(3):
            TEST_DATA['id'] = str(uuid.uuid4())
            es_data.append(deepcopy(TEST_DATA))
        TEST_DATA['id'] = str(uuid.uuid4())
        TEST_DATA['imdb_rating'] = 15
        es_data.append(deepcopy(TEST_DATA))
        TEST_DATA['id'] = str(uuid.uuid4())
        TEST_DATA['imdb_rating'] = -2
        es_data.append(deepcopy(TEST_DATA))
        TEST_DATA['id'] = '1123456'
        TEST_DATA['imdb_rating'] = 5
        es_data.append(deepcopy(TEST_DATA))

    if type_test == 'phrase':
        for _ in range(3):
            TEST_DATA['id'] = str(uuid.uuid4())
            TEST_DATA['title'] = 'The Star'
            es_data.append(deepcopy(TEST_DATA))
        for _ in range(3):
            TEST_DATA['id'] = str(uuid.uuid4())
            TEST_DATA['title'] = 'Star Roger'
            es_data.append(deepcopy(TEST_DATA))
        TEST_DATA['id'] = str(uuid.uuid4())
        TEST_DATA['title'] = 'Roger Philips'
        es_data.append(deepcopy(TEST_DATA))

    bulk_query: list[dict] = []

    for row in es_data:
        data = {'_index': test_settings.es_index, '_id': row['id']}
        data.update({'_source': row})
        bulk_query.append(data)

    return bulk_query


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    t = type(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict]) -> None:
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(
            index=test_settings.es_index,
        )

        updated, errors = await async_bulk(client=es_client, actions=data)

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(session_client):
    async def inner(type_api, query_data) -> Response:
        url = test_settings.service_url + '/api/v1/' + type_api + '/'
        query_data = {'query': query_data[type_api]}
        async with session_client.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        return Response(body, headers, status)

    return inner


@pytest_asyncio.fixture(name="es_add_film")
def es_add_film(es_client: AsyncElasticsearch):
    async def inner():
        test_film = deepcopy(TEST_DATA)
        test_film['id'] = test_settings.es_id_field
        film = await es_client.index(index=test_settings.es_index, id=test_film['id'], body=test_film)
        print(film)
        print(film)
        print(film)
        print(film)
        print(film)
        print(film)
        return film
    return inner
    # await es_client.delete(index=test_settings.es_index, id=test_film['id'])
