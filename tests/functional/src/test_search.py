import orjson
import pytest
import time

from redis.asyncio.client import Redis

from tests.functional.conftest import (es_write_data, event_loop, es_data,
                                       make_get_request, es_client, session_client, flush_redis,
                                       redis_write_data, redis_client, es_data_redis)
from tests.functional.testdata.data import PARAMETRES


#
# @pytest.mark.parametrize(
#     'query_data, expected_answer',
#     PARAMETRES['limit']
# )
# @pytest.mark.fixt_data('limit')
# @pytest.mark.asyncio
# async def test_search_limit(
#         es_write_data,
#         make_get_request,
#         es_data: list[dict],
#         query_data: dict,
#         expected_answer: dict
# ) -> None:
#     """
#     Проверка, что поиск по названию фильма
#     возвращает только первые 10 результатов
#     :return:
#     """
#     # Загружаем данные в ES
#     await es_write_data(es_data)
#     # time.sleep(1)
#     response = await make_get_request('films/search', query_data)
#
#     # Проверяем ответ
#     assert response.status == expected_answer['status']
#     assert len(response.body) == expected_answer['length']
#
#
# @pytest.mark.parametrize(
#     'query_data, expected_answer',
#     PARAMETRES['validation']
# )
# @pytest.mark.fixt_data('validation')
# @pytest.mark.asyncio
# async def test_search_validation(
#         es_write_data,
#         make_get_request,
#         es_data,
#         query_data: dict,
#         expected_answer: dict
# ) -> None:
#     # Загружаем данные в ES
#     await es_write_data(es_data)
#     # time.sleep(1)
#     response = await make_get_request('films/search', query_data)
#
#     # Проверяем ответ
#     assert response.status == expected_answer['status']
#     assert len(response.body) == expected_answer['length']
#
#
# @pytest.mark.parametrize(
#     'query_data, expected_answer',
#     PARAMETRES['phrase']
# )
# @pytest.mark.fixt_data('phrase')
# @pytest.mark.asyncio
# async def test_search_phrase(
#         es_write_data,
#         make_get_request,
#         es_data,
#         query_data: dict,
#         expected_answer: dict
# ) -> None:
#     # Загружаем данные в ES
#     await es_write_data(es_data)
#     # time.sleep(1)
#     response = await make_get_request('films/search', query_data)
#
#     # Проверяем ответ
#     assert response.status == expected_answer['status']
#     assert len(response.body) == expected_answer['length']


@pytest.mark.asyncio
async def test_search_with_cache(
        redis_write_data,
        make_get_request,
        es_data_redis: list[dict],
        redis_client: Redis
):
    # Prepare the data
    data = {f"movies:{film['id']}": film for film in es_data_redis}

    # Write data to Redis
    await redis_write_data(data)

    # Perform the API request
    response = await make_get_request('search', {'query': 'Star'})

    # Validate the response
    assert response.status == 200
    assert len(response.body) > 0
    assert all('Star' in film['title'] for film in response.body)

    # Check that data was retrieved from Redis
    for film in response.body:
        assert await redis_client.exists(f"movies:{film['id']}")
