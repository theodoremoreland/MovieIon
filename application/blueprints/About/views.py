from flask import Blueprint, render_template

about = Blueprint(
    "about", __name__, template_folder="templates", static_folder="static"
)


@about.route("/about")
def display_about_page():
    """
    Handles request to display About page.
    """

    return render_template("about.html")
