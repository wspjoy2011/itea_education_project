error_401_example = {
  "detail": "Authentication credentials were not provided."
}

error_403_example = {
  "detail": "You do not have permission to perform this action."
}

error_movie_400_required_fields_example = {
  "errors": {
    "name": [
      "This field is required."
    ],
    "year": [
      "This field is required."
    ],
    "time": [
      "This field is required."
    ],
    "imdb": [
      "This field is required."
    ],
    "votes": [
      "This field is required."
    ],
    "description": [
      "This field is required."
    ],
    "certification_id": [
      "This field is required."
    ],
    "genre_ids": [
      "This field is required."
    ],
    "director_ids": [
      "This field is required."
    ],
    "star_ids": [
      "This field is required."
    ]
  }
}

error_movie_400_unique_constrain_example = {
  "errors": {
    "non_field_errors": [
      "The fields name, year, time must make a unique set."
    ]
  }
}