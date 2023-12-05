import json
import pg8000

from modules.config import user, password, host, port, database

PATH = "db/movie_title_to_id_mapping.json"


def get_movies_json():
    try:
        f = open(PATH)

        print(f"SUCCESS: Loaded {PATH}!\n")

        return json.load(f)
    except Exception as e:
        print(e)

        return None


def create_movies_json(movie_title_to_id_mapping):
    try:
        with open(PATH, "w") as outfile:
            json.dump(movie_title_to_id_mapping, outfile)

            print(f"SUCCESS: {PATH} created!\n")
    except Exception as e:
        print(f"ERROR: Failed to create {PATH} - {e}\n")


def database_cursor():
    """
    Establishes connection with database and returns cursor object.

    Returns:
        cursor (object): Cursor object for database.
    """

    try:
        connection = pg8000.connect(
            user=user, password=password, host=host, port=int(port), database=database
        )
        cursor = connection.cursor()

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

        return cursor
    except Exception as error:
        print("Error while connecting to PostgreSQL database", error)


def get_all_movies(cursor, movies_json):
    """
    Gets all movies from database.

    Returns:
        movie_title_to_id_mapping (dict): Dictionary mapping movie titles to their respective movie ids.
    """

    """
    movie_title_to_id_mapping is a dictionary that maps movie titles to their respective movie ids.

    Example: movie_title_to_id_mapping = { "Toy Story (1995)": 1, "Jumanji (1995)": 2, ... }
    """
    movie_title_to_id_mapping = movies_json if movies_json != None else {}

    if movie_title_to_id_mapping == False:
        try:
            cursor.execute("SELECT title, movie_id FROM movie_list;")
            all_movies = cursor.fetchall()

            for _, (movie_title, movie_id) in enumerate(all_movies):
                movie_title_to_id_mapping[movie_title] = movie_id

            return movie_title_to_id_mapping

        except Exception as error:
            print("Error while selecting rows(title, movie_id)", error)
    else:
        return movie_title_to_id_mapping


cursor = database_cursor()
movies_json = get_movies_json()
movie_title_to_id_mapping = get_all_movies(cursor, movies_json)

if movies_json == None and movie_title_to_id_mapping != None:
    create_movies_json(movie_title_to_id_mapping)
