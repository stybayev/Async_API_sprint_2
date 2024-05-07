from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    es_index: str = Field(default='movies')
    es_id_field: str = Field(default='ffc3df9f-a17e-4bae-b0b6-c9c4da290fdd')
    redis_host: str = Field(default='localhost', env='REDIS_HOST')
    service_url: str = Field(default='http://127.0.0.1:8000', env='SERVICE_URL')
    # es_mapping = {
    #     "movies": {
    #         "mappings": {
    #             "dynamic": "strict",
    #             "properties": {
    #                 "actors": {
    #                     "type": "nested",
    #                     "dynamic": "strict",
    #                     "properties": {
    #                         "id": {
    #                             "type": "keyword"
    #                         },
    #                         "name": {
    #                             "type": "text",
    #                             "analyzer": "ru_en"
    #                         }
    #                     }
    #                 },
    #                 "actors_names": {
    #                     "type": "text",
    #                     "fields": {
    #                         "raw": {
    #                             "type": "keyword"
    #                         }
    #                     },
    #                     "analyzer": "ru_en"
    #                 },
    #                 "description": {
    #                     "type": "text",
    #                     "analyzer": "ru_en"
    #                 },
    #                 "director": {
    #                     "dynamic": "strict",
    #                     "properties": {
    #                         "id": {
    #                             "type": "keyword"
    #                         },
    #                         "name": {
    #                             "type": "text",
    #                             "fields": {
    #                                 "raw": {
    #                                     "type": "keyword"
    #                                 }
    #                             },
    #                             "analyzer": "ru_en"
    #                         }
    #                     }
    #                 },
    #                 "genre": {
    #                     "type": "keyword"
    #                 },
    #                 "id": {
    #                     "type": "keyword"
    #                 },
    #                 "imdb_rating": {
    #                     "type": "float"
    #                 },
    #                 "title": {
    #                     "type": "text",
    #                     "fields": {
    #                         "raw": {
    #                             "type": "keyword"
    #                         }
    #                     },
    #                     "analyzer": "ru_en"
    #                 },
    #                 "writers": {
    #                     "type": "nested",
    #                     "dynamic": "strict",
    #                     "properties": {
    #                         "id": {
    #                             "type": "keyword"
    #                         },
    #                         "name": {
    #                             "type": "text",
    #                             "analyzer": "ru_en"
    #                         }
    #                     }
    #                 },
    #                 "writers_names": {
    #                     "type": "text",
    #                     "fields": {
    #                         "raw": {
    #                             "type": "keyword"
    #                         }
    #                     },
    #                     "analyzer": "ru_en"
    #                 }
    #             }
    #         }
    #     },
    #     "persons": {
    #         "mappings": {
    #             "dynamic": "strict",
    #             "properties": {
    #                 "full_name": {
    #                     "type": "text",
    #                     "fields": {
    #                         "raw": {
    #                             "type": "keyword"
    #                         }
    #                     }
    #                 },
    #                 "id": {
    #                     "type": "keyword"
    #                 }
    #             }
    #         }
    #     },
    #     "genres": {
    #         "mappings": {
    #             "dynamic": "strict",
    #             "properties": {
    #                 "description": {
    #                     "type": "text"
    #                 },
    #                 "id": {
    #                     "type": "keyword"
    #                 },
    #                 "name": {
    #                     "type": "text",
    #                     "fields": {
    #                         "raw": {
    #                             "type": "keyword"
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     }
    # }


test_settings = TestSettings()
