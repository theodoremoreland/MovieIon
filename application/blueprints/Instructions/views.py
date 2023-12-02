from flask import Blueprint, render_template

instructions = Blueprint(
    "instructions", __name__, template_folder="templates", static_folder="static"
)


@instructions.route("/instructions")
def display_instructions_page():
    """
    Handles request to display Instructions page.
    """

    return render_template("instructions.html")
