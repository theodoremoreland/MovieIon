import ast

from flask import Blueprint, render_template

from db import DB
from modules.logger import logger

movie_info = Blueprint(
    "movie_info", __name__, template_folder="templates", static_folder="static"
)


@movie_info.route("/info/<movie_id>", methods=["GET"])
def display_movie_info(movie_id):
    """
    Handles request to display movie information.

    Args: movie_id (str): Identifier of movie to be displayed.
    """
    logger.debug(f"Received GET request to /info/{movie_id}")

    try:
        cursor = DB.cursor
        movie_id = int(movie_id)

        if movie_id > 114554 or movie_id < 2:
            raise ValueError(f"Invalid movie_id: {movie_id}")

        cursor.execute(f"SELECT * FROM metadata WHERE id = '{movie_id}';")
        metadata = cursor.fetchone()

        title = metadata[1]
        overview = metadata[2]
        crew = ast.literal_eval(metadata[3])  # list of tuples
        cast = ast.literal_eval(metadata[4])  # list
        genres = ast.literal_eval(metadata[5])  # list
        language = metadata[6]
        runtime = metadata[7]
        budget = metadata[8]
        revenue = metadata[9]

        return render_template(
            "info.html",
            movie_id=movie_id,
            title=title,
            overview=overview,
            crew=crew,
            cast=cast,
            genres=genres,
            language=language,
            runtime=runtime,
            budget=budget,
            revenue=revenue,
        )
    except Exception as e:
        logger.exception(f"ERROR @ display_movie_info: {e}")

        return render_template("error.html")
