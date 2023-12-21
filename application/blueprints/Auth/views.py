from flask import Blueprint, render_template, request, redirect, session, flash

from db import DB
from modules.logger import logger

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route("/login", methods=["POST", "GET"])
def login():
    """
    Handles request to log in user. Redirects to profile page if successful.
    """

    if request.method == "POST":
        logger.debug("Received POST request to /login")

        try:
            cursor = DB.cursor
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
                    flash("Invalid username.")
            else:
                flash("Invalid username.")
        except Exception as e:
            logger.exception(f"ERROR @ login: {e}")

            return render_template("error.html")

    logger.debug("Received GET request to /login")

    return render_template("login.html")


@auth.route("/logout")
def logout():
    """
    Handles request to log out user. Redirects to login page.
    """
    logger.debug("Received request to /logout")

    if "username" in session:
        username = session["username"]
        del session["username"]
        flash(f"{username} is now logged out")
    else:
        flash("You need to log in before you can log out")

    return redirect("/login")
