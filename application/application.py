# Third party
from flask import Flask

# Custom
from modules.config import secret_key

# Blueprints
from blueprints.Home.views import home
from blueprints.Auth.views import auth
from blueprints.MovieInfo.views import movie_info
from blueprints.Profile.views import profile
from blueprints.About.views import about
from blueprints.Instructions.views import instructions


application = Flask(__name__)
application.config["DEBUG"] = False
application.secret_key = secret_key
application.register_blueprint(home)
application.register_blueprint(auth)
application.register_blueprint(movie_info)
application.register_blueprint(profile)
application.register_blueprint(about)
application.register_blueprint(instructions)


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
