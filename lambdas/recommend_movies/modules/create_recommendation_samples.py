# Native
import random

# Custom
from modules.transform_recommendation_data import transform_recommendation_data
from modules.model import model_knn, movie_matrix, movie_title_index


def create_recommendation_samples(
    movies, movie_title_to_id_mapping, make_recommendations
):
    """
    Creates recommendation samples for each movie selection. Each sample contains 5 random recommendations.

    Args:
        movies (list of dict): List of movie objects.
        movie_title_to_id_mapping (dict of str: int): Dictionary mapping movie titles to their respective movie ids (ex: { "Toy Story (1995)": 1, "Jumanji (1995)": 2, ... }).
        make_recommendations (function): Callback function that returns a list of recommendations based on a given movie.

    Returns:
        recommendations (list of list): 2d list of recommendations for each movie selection resulting in 3 lists of 5 recommendations.
    """
    recommendations = {
        "based_on_movie_1": [],
        "based_on_movie_2": [],
        "based_on_movie_3": [],
    }

    recommendations["based_on_movie_1"] = make_recommendations(
        model_knn=model_knn,
        data=movie_matrix,
        fav_movie=movies[0]["movie_title"],
        mapper=movie_title_index,
        n_recommendations=10,
    )  # example value: [('Screamers (1995)', 0.0), ('Two if by Sea (1996)', 0.0), ('Georgia (1995)', 0.0)]

    recommendations["based_on_movie_2"] = make_recommendations(
        model_knn=model_knn,
        data=movie_matrix,
        fav_movie=movies[1]["movie_title"],
        mapper=movie_title_index,
        n_recommendations=10,
    )

    recommendations["based_on_movie_3"] = make_recommendations(
        model_knn=model_knn,
        data=movie_matrix,
        fav_movie=movies[2]["movie_title"],
        mapper=movie_title_index,
        n_recommendations=10,
    )

    # Select 5 random recommendations from each movie
    recommendation_sample_movie_1 = random.sample(
        recommendations["based_on_movie_1"], 5
    )  # example value: [('Screamers (1995)', 0.0), ('Two if by Sea (1996)', 0.0), ('Georgia (1995)', 0.0)]
    recommendation_sample_movie_2 = random.sample(
        recommendations["based_on_movie_2"], 5
    )
    recommendation_sample_movie_3 = random.sample(
        recommendations["based_on_movie_3"], 5
    )

    recommendation_sample_movie_1 = map(
        lambda recommendation: transform_recommendation_data(
            recommendation, movie_title_to_id_mapping
        ),
        recommendation_sample_movie_1,
    )
    # Example value: [{'movie_title': 'Screamers (1995)', 'movie_distance': 0.0, 'movie_id': 1}, {'movie_title': 'Two if by Sea (1996)', 'movie_distance': 0.0, 'movie_id': 2}, {'movie_title': 'Georgia (1995)', 'movie_distance': 0.0, 'movie_id': 3}]
    recommendation_sample_movie_2 = map(
        lambda recommendation: transform_recommendation_data(
            recommendation, movie_title_to_id_mapping
        ),
        recommendation_sample_movie_2,
    )
    recommendation_sample_movie_3 = map(
        lambda recommendation: transform_recommendation_data(
            recommendation, movie_title_to_id_mapping
        ),
        recommendation_sample_movie_3,
    )

    return [
        list(recommendation_sample_movie_1),
        list(recommendation_sample_movie_2),
        list(recommendation_sample_movie_3),
    ]
