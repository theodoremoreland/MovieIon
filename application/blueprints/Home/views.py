from flask import Blueprint, render_template, redirect, request, jsonify

from db import all_movies, movie_title_to_id_mapping
from modules.create_recommendation_samples import create_recommendation_samples
from modules.model import best_recommendations, worst_recommendations

home = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@home.route("/", methods=["GET"])
def index():
    """
    Handles request to display home page.
    """

    return render_template("index.html", all_movies=all_movies)


@home.route("/choices", methods=["POST", "GET"])
def make_positive_recommendations():
    """
    Handles request to get positive recommendations (i.e. movies the user will enjoy)
    based on their 3 movie choices. Redirects to root if request is GET request.
    """

    if request.method == "POST":
        movies = (
            request.get_json()
        )  # example value: [{ "movie_title": "Toy Story (1995)", "movie_id": 1 }, ...]

        [
            recommendation_sample_movie_1,
            recommendation_sample_movie_2,
            recommendation_sample_movie_3,
        ] = create_recommendation_samples(
            movies, movie_title_to_id_mapping, best_recommendations
        )

        return jsonify(
            {
                "data": render_template(
                    "recommended.html",
                    recommendation_sample_movie_1=list(recommendation_sample_movie_1),
                    recommendation_sample_movie_2=list(recommendation_sample_movie_2),
                    recommendation_sample_movie_3=list(recommendation_sample_movie_3),
                    movies=movies,
                )
            }
        )

    return redirect("/")


@home.route("/worst", methods=["POST", "GET"])
def make_negative_recommendations():
    """
    Handles request for getting negative recommendations (i.e. movies the user will dislike)
    based on their 3 movie choices. Redirects to root if request is GET request.
    """

    if request.method == "POST":
        movies = (
            request.get_json()
        )  # example value: [{ "movie_title": "Toy Story (1995)", "movie_id": 1 }, ...]

        [
            recommendation_sample_movie_1,
            recommendation_sample_movie_2,
            recommendation_sample_movie_3,
        ] = create_recommendation_samples(
            movies, movie_title_to_id_mapping, worst_recommendations
        )

        return jsonify(
            {
                "data": render_template(
                    "worst.html",
                    recommendation_sample_movie_1=list(recommendation_sample_movie_1),
                    recommendation_sample_movie_2=list(recommendation_sample_movie_2),
                    recommendation_sample_movie_3=list(recommendation_sample_movie_3),
                    movies=movies,
                )
            }
        )

    return redirect("/")
