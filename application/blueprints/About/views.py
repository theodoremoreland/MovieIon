from flask import Blueprint, render_template

from modules.logger import logger

about = Blueprint(
    "about", __name__, template_folder="templates", static_folder="static"
)


@about.route("/about", methods=["GET"])
def display_about_page():
    """
    Handles request to display About page.
    """
    logger.debug("Received GET request to /about")

    return render_template("about.html")
