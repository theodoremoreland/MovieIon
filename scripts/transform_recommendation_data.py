def transform_recommendation_data(recommendation, movie_title_to_id_mapping):
    """
    Transforms recommendation data from form: [('Screamers (1995)', 0.0), ('Two if by Sea (1996)', 0.0), ('Georgia (1995)', 0.0)]
    To form: [['Screamers (1995)', 0.0, 1], ['Two if by Sea (1996)', 0.0, 2], ['Georgia (1995)', 0.0, 3]]

    Args: recommendation (tuple): The recommendation data to be transformed (e.g. ('Screamers (1995)', 0.0))

    Returns: list: The transformed recommendation data (e.g. ['Screamers (1995)', 0.0, 1])
    """

    # pprint(list(movie_title_to_id_mapping.keys())[0:5])

    movie_title = recommendation[0]
    movie_distance = recommendation[1]
    movie_id = movie_title_to_id_mapping.get(movie_title)

    return {
        "movie_title": movie_title,
        "movie_distance": movie_distance,
        "movie_id": movie_id,
    }
