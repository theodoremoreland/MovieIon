from flask import Blueprint, render_template, redirect, session, flash, jsonify

from db import DB

profile = Blueprint(
    "profile", __name__, template_folder="templates", static_folder="static"
)


@profile.route("/profile/<username>", methods=["POST", "GET"])
def render_profile(username):
    """
    Handles request to display user profile page.

    Args: username (str): The username of the user whose profile is to be displayed.
    """

    watchlist = []

    if "username" in session:
        if username == "user":
            username = session["username"]
    else:
        return redirect("/login")

    try:
        cursor = DB.cursor

        cursor.execute(f"SELECT watchlist FROM users WHERE username = '{username}';")
        watchlist_ids = (
            cursor.fetchone()
        )  # Returns 2d array wherein first and singular element contains actual data.

        for movie_id in watchlist_ids[0]:
            cursor.execute(
                f"SELECT title FROM movie_list WHERE movie_id = '{movie_id}';"
            )
            movie_title = cursor.fetchone()[0]
            watchlist.append({"movie_id": movie_id, "movie_title": movie_title})

        return render_template("profile.html", watchlist=watchlist, username=username)

    except Exception as error:
        print("ERROR: Error while querying database", error)

        return render_template("error.html")


# TODO this route should just handle POST requests, but would require a form or event listener/handler to be implemented.
@profile.route("/watchlist/<movie_id>", methods=["POST", "GET"])
def add_to_watchlist(movie_id):
    """
    Handles request to add a movie to the user's watchlist.

    Args: movie_id (str): The movie to be added to the user's watchlist.
    """

    try:
        cursor = DB.cursor
        movie_id = int(movie_id)  # Confirm id is an integer.

        cursor.execute(f"SELECT title FROM movie_list WHERE movie_id = '{movie_id}';")
        movie = cursor.fetchone()[0]
        username = session["username"]
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            f"UPDATE users SET watchlist = array_append(watchlist, '{movie_id}') WHERE username = '{username}';"
        )
        cursor.execute("COMMIT;")
        flash(f"{movie} successfully added to watchlist!")

        return redirect(f"/info/{movie_id}")

    except Exception as error:
        print("Error while querying database", error)
        flash("There was an error when attempting to add to watchlist.")

        return redirect(f"/info/{movie_id}")


# TODO this route should just handle POST requests, but would require a form or event listener/handler to be implemented.
@profile.route("/remove/<movie_id>", methods=["POST", "GET"])
def remove_from_watchlist(movie_id):
    """
    Handles request to remove a movie from the user's watchlist.

    Args: movie_id (str): The movie to be removed from the user's watchlist.
    """

    try:
        cursor = DB.cursor
        movie_id = int(movie_id)  # Confirm id is an integer.
        username = session["username"]

        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(
            f"UPDATE users SET watchlist = array_remove(watchlist, '{movie_id}') WHERE username = '{username}';"
        )
        cursor.execute("COMMIT;")
    except Exception as error:
        print("Error while querying database", error)

    return redirect(f"/profile/{username}")
