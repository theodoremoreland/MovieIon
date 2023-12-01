# Native library
import ast

# Third party
import pg8000
from flask import Flask, render_template, request, redirect, session, flash, jsonify

# Custom
from scripts.create_recommendation_samples import create_recommendation_samples
from scripts.model import best_recommendations, worst_recommendations
from scripts.config import user, password, host, port, database, secret_key

application = Flask(__name__)
application.config["DEBUG"] = True
application.secret_key = secret_key


@application.before_first_request
def setup():
    """
    Will establish connection to database and create cursor object prior to
    handling first HTTP request. Also creates movie_title_to_id_mapping dictionary and cursor object
    for global scope.
    """

    global cursor, movie_title_to_id_mapping

    """
    movie_title_to_id_mapping is a dictionary that maps movie titles to their respective movie ids.

    Example: movie_title_to_id_mapping = { "Toy Story (1995)": 1, "Jumanji (1995)": 2, ... }
    """
    movie_title_to_id_mapping = {}

    try:
        connection = pg8000.connect(
            user=user, password=password, host=host, port=int(port), database=database
        )
        cursor = connection.cursor()

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except Exception as error:
        print("Error while connecting to PostgreSQL database", error)
        connection = pg8000.connect(
            user=user, password=password, host=host, port=int(port), database=database
        )

        cursor = connection.cursor()


@application.route("/", methods=["POST", "GET"])
def index():
    """
    Handles request to display home page. Attempts to fetch list of movies
    from database for user selection.
    """

    global cursor, movie_title_to_id_mapping

    try:
        cursor.execute("SELECT title, movie_id FROM movie_list;")
        all_movies = cursor.fetchall()

        for _, (movie_title, movie_id) in enumerate(all_movies):
            movie_title_to_id_mapping[movie_title] = movie_id
            # pprint(movie_title_to_id_mapping)

    except Exception as error:
        print("Error while selecting rows(title, movie_id)", error)

    return render_template("index.html", all_movies=all_movies)


@application.route("/instructions")
def instructions():
    """
    Handles request to display Instructions page.
    """

    return render_template("instructions.html")


@application.route("/about")
def about():
    """
    Handles request to display About page.
    """

    return render_template("about.html")


@application.route("/login", methods=["POST", "GET"])
def login():
    """
    Handles request to log in user. Redirects to profile page if successful.
    """

    global cursor

    if request.method == "POST":
        username = request.form["username"]
        cursor.execute(
            f"SELECT user_id, username, watchlist FROM users WHERE username = '{username}';"
        )  # postgres can only interpret single quoted strings
        user_info = cursor.fetchone()

        if user_info:
            if user_info[1] == username:
                session["username"] = username

                return redirect(f"/profile/{username}")
            else:
                flash("Invalid username")
        else:
            flash("Invalid username")

    return render_template("login.html")


@application.route("/logout")
def logout():
    """
    Handles request to log out user. Redirects to login page.
    """

    if "username" in session:
        username = session["username"]
        del session["username"]
        flash(f"{username} is now logged out")
    else:
        flash("You need to log in before you can log out")

    return redirect("/login")


@application.route("/profile/<username>", methods=["POST", "GET"])
def render_profile(username):
    """
    Handles request to display user profile page.

    Args: username (str): The username of the user whose profile is to be displayed.
    """

    global cursor

    if "username" in session:
        if username == "user":
            username = session["username"]
    else:
        return redirect("/login")

    try:
        cursor.execute(f"SELECT watchlist FROM users WHERE username = '{username}';")
        watchlist = (
            cursor.fetchone()
        )  # Returns 2d array wherein first and singular element contains actual data.
        movie_ids = []

        for movie in watchlist[0]:
            cursor.execute(f"SELECT movie_id FROM movie_list WHERE title = '{movie}';")
            movie_id = cursor.fetchone()[0]
            movie_ids.append(movie_id)

        return render_template(
            "profile.html", movieIDs=movie_ids, watchlist=watchlist, username=username
        )

    except Exception as error:
        print("Error while querying database", error)

    return render_template(
        "profile.html", movieIDs=[[]], watchlist=[[]], username=username
    )  # 2d arrays simulate a null return from queries


@application.route("/info/<movie_id>")
def display_movie_info(movie_id):
    """
    Handles request to display movie information.

    Args: movie_id (str): Identifier of movie to be displayed.
    """

    global cursor

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


@application.route("/watchlist/<movie_id>", methods=["POST", "GET"])
def add_to_watchlist(movie_id):
    """
    Handles request to add a movie to the user's watchlist.

    Args: movie_id (str): The movie to be added to the user's watchlist.
    """

    global cursor

    try:
        cursor.execute(f"SELECT title FROM movie_list WHERE movie_id = '{movie_id}';")
        movie = cursor.fetchone()[0]
        movie = movie.replace(",", ",,")
        movie = movie.replace("'", "''")
        username = session["username"]
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            f"UPDATE users SET watchlist = array_append(watchlist, '{movie}') WHERE username = '{username}';"
        )
        cursor.execute("COMMIT;")
        cursor.execute(f"SELECT watchlist FROM users WHERE username = '{username}';")
        recently_added_to_watchlist = cursor.fetchone()[0][-1]
        flash(f"{recently_added_to_watchlist} successfully added to watchlist!")

        return redirect(f"/info/{movie_id}")

    except Exception as error:
        print("Error while querying database", error)
        flash("There was an error when attempting to add to watchlist.")

        return redirect(f"/info/{movie_id}")


@application.route("/remove/<movie>", methods=["POST", "GET"])
def remove_from_watchlist(movie):
    """
    Handles request to remove a movie from the user's watchlist.

    Args: movie (str): The movie to be removed from the user's watchlist.
    """

    global cursor

    movie = movie.replace(",", ",,")
    movie = movie.replace("'", "''")

    try:
        username = session["username"]
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            f"UPDATE users SET watchlist = array_remove(watchlist, '{movie}') WHERE username = '{username}';"
        )
        cursor.execute("COMMIT;")
    except Exception as error:
        print("Error while querying database", error)

    return redirect(f"/profile/{username}")


@application.route("/choices", methods=["POST", "GET"])
def make_positive_recommendations():
    """
    Handles request to get positive recommendations (i.e. movies the user will enjoy)
    based on their 3 movie choices. Redirects to root if request is GET request.
    """

    global cursor, movie_title_to_id_mapping

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


@application.route("/worst", methods=["POST", "GET"])
def make_negative_recommendations():
    """
    Handles request for getting negative recommendations (i.e. movies the user will dislike)
    based on their 3 movie choices. Redirects to root if request is GET request.
    """

    global cursor, movie_title_to_id_mapping

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


if __name__ == "__main__":
    application.run()
