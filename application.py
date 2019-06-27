import psycopg2
from psycopg2 import Error
from flask import (Flask, render_template)
from flask_sqlalchemy import SQLAlchemy
from config import (user, password, host, port, database)

try:
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

application = Flask(__name__)
# Remember to change this when deploying
application.config['DEBUG'] = True

# Create database tables
# @application.before_first_request
# def setup():
#     return None


@application.route("/")
def index():
    return render_template("index.html")


@application.route("/movie")
def movie():

    return render_template("movie.html")


@application.route("/recommended")
def recommended():

    return render_template("recommended.html")


if __name__ == "__main__":
    application.run()
