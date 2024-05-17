TEST_DATA = {
    'id': 'ffc3df9f-a17e-4bae-b0b6-c9c4da290fdd',
    'imdb_rating': 8.5,
    'genre': ['Action', 'Sci-Fi'],
    'title': 'The Star',
    'description': 'New World',
    'director': {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
    'actors_names': ['Ann', 'Bob'],
    'writers_names': ['Ben', 'Howard'],
    'actors': [
        {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
        {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
    ],
    'writers': [
        {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
        {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
    ]
}

TEST_DATA_GENRE = {
    'id': 'adb5ffa8-7dbc-4088-8e5f-44311680a75c',
    'name': 'Action',
    'description': 'description'
}

TEST_DATA_PERSON = {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'full_name': 'Ann'}

PARAMETERS = {
    'phrase': [
        (
            {'films/search': 'Star'},
            {'status': 200, 'length': 6}
        ),
        (
            {'films/search': 'Roger'},
            {'status': 200, 'length': 4}
        ),
        (
            {'films/search': 'Philips'},
            {'status': 200, 'length': 1}
        )
    ],
    'limit': [
        (
            {'films/search': 'The Star'},
            {'status': 200, 'length': 10}
        ),
        (
            {'films/search': 'Marched Potato'},
            {'status': 200, 'length': 0}
        )
    ],
    'validation': [
        (
            {'films/search': 'The Star'},
            {'status': 200, 'length': 3}
        ),
    ],
    'redis_search': [
        (
            {'films/search': 'Star'},
            {'status': 200, 'length': 6}
        )
    ],
    'redis_films': [
        (
            {'films/': 'Star'},
            {'status': 200, 'length': 6}
        )
    ],

    'redis_films_id': [
        (
            {'id': 'ffc3df9f-a17e-4bae-b0b6-c9c4da290fdd'},
            {
                'status': 200,
                'title': 'The Star',
                'id': 'ffc3df9f-a17e-4bae-b0b6-c9c4da290fdd'
            }
        )
    ],
    'redis_genre': [
        (
            {'genres': '', 'id': 'adb5ffa8-7dbc-4088-8e5f-44311680a75c'},
            {
                'status': 200,
                'name': 'Action',
                'id': 'adb5ffa8-7dbc-4088-8e5f-44311680a75c'
            }
        )
    ],
    'redis_person': [
        (
            {'persons': '', 'id': TEST_DATA_PERSON['id']},
            {
                'status': 200,
                'full_name': 'Ann',
                'id': TEST_DATA_PERSON['id']
            }
        )
    ],
    'film_search': [
        (
            {
                'id': 'ffc3df9f-a17e-4bae-b0b6-c9c4da290fdd',
                'films': ''
            },
            {
                'status': 200,
                'id': 'ffc3df9f-a17e-4bae-b0b6-c9c4da290fdd'
            }
        ),
        (
            {
                'id': 'ffc3df9f-a17e-4bae-b0b6-c9c4da290fde',
                'films': ''
            },
            {
                'status': 404,
                'answer': 'film not found'
            }
        )
    ],
    'limit_genres': [
        (
            {'genres': ''},
            {'status': 200, 'length': 10}
        )
    ],
    'limit_persons': [
        (
            {'persons': ''},
            {'status': 200, 'length': 10}
        )
    ],

    'all_films': [
        (
            {'films': ''},
            {'status': 200, 'length': 10}
        )
    ],

    'search_genre': [
        (
            {
                'id': 'adb5ffa8-7dbc-4088-8e5f-44311680a75c',
                'genres': '',
            },
            {
                'status': 200,
                'length': 1,
                'name': 'Action',
                'id': 'adb5ffa8-7dbc-4088-8e5f-44311680a75c'
            }
        ),
        (
            {
                'id': 'adb5ffa8-7dbc-4088-8e5f-44311680a76c',
                'genres': ''
            },
            {
                'status': 404,
                'answer': 'genre not found'
            }
        )
    ],
    'search_person': [
        (
            {
                'id': TEST_DATA_PERSON['id'],
                'persons': '',
            },
            {
                'status': 200,
                'answer': TEST_DATA_PERSON
            }
        )
    ],
    'genre_validation': [
        (
            {'genres': ''},
            {'status': 200, 'length': 3}
        )
    ],
    'films_validation': [
        (
            {'films': ''},
            {'status': 200, 'length': 3}
        )
    ],
    'person_validation': [
        (
            {'persons': ''},
            {'status': 200, 'length': 3}
        )
    ],
    'person_films': [
        (
            {'id': f'{TEST_DATA_PERSON["id"]}/film?page_size=100&page_number=1'},
            {'status': 200, 'length': 15}
        )
    ]
}
