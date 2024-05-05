import uuid
import datetime

TEST_DATA = {
    'id': str(uuid.uuid4()),
    'imdb_rating': 8.5,
    'genre': ['Action', 'Sci-Fi'],
    'title': 'The Star',
    'description': 'New World',
    'director': ['Stan'],
    'actors_names': ['Ann', 'Bob'],
    'writers_names': ['Ben', 'Howard'],
    'actors': [
        {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
        {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
    ],
    'writers': [
        {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
        {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
    ],
    'created_at': datetime.datetime.now().isoformat(),
    'updated_at': datetime.datetime.now().isoformat(),
    'film_work_type': 'movie'
}

PARAMETRES = {
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
    ]
}
