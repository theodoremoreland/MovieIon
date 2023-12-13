from flask import Blueprint, render_template

from modules.logger import logger

instructions = Blueprint(
    "instructions", __name__, template_folder="templates", static_folder="static"
)


@instructions.route("/instructions", methods=["GET"])
def display_instructions_page():
    """
    Handles request to display Instructions page.
    """
    logger.debug("Received GET request to /instructions")

    return render_template("instructions.html")
