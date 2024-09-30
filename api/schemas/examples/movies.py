movie_detail_example = {
    "uuid": "0d8b3251-203b-4843-a61f-d7ba569116a5",
    "name": "The Last Boy",
    "year": 2019,
    "time": 87,
    "imdb": 4.9,
    "votes": 10324,
    "meta_score": None,
    "gross": None,
    "description": "With the world's end imminent, a dying mother sends her young son on a journey to the place which grants wishes. The film's inspired by the works of 13th century Sufi mystic and poet, Rumi.",
    "slug": "the-last-boy",
    "certification": "Not Rated",
    "genres": [
        "Mystery",
        "Fantasy",
        "Sci-Fi"
    ],
    "directors": [
        "Perry Bhandal"
    ],
    "stars": [
        "Luke Goss",
        "Flynn Allen",
        "Peter Guinness",
        "Matilda Freeman"
    ]
}

movie_create_example = {
    "name": "Casablanca (Example)",
    "year": 1942,
    "time": 102,
    "imdb": 8.5,
    "votes": 592666,
    "meta_score": 100.0,
    "gross": 1020000.0,
    "description": "A cynical expatriate American cafe owner struggles to decide whether or not to help his former lover and her fugitive husband escape the Nazis in French Morocco.",
    "certification_id": 28,
    "genre_ids": [
        33, 34
    ],
    "director_ids": [
        4358, 4357
    ],
    "star_ids": [
        15364, 15367
    ]
}


movie_example_response_json = {
    "previous": None,
    "next": "http://127.0.0.1:8001/api/v1.0/movies/?page=2",
    "pages": 2500,
    "count": 10000,
    "results": [
        movie_detail_example
    ]
}
