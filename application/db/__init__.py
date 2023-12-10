import json
import pg8000

from modules.config import user, password, host, port, database

PATH = "db/movie_title_to_id_mapping.json"


class _Database:
    def __init__(self):
        self._cursor = None

    @property
    def cursor(self):
        """
        If cursor hasn't been created, establishes connection with database and reassigns cursor object
        before returning it. Else, returns cursor object.

        If connection attempt fails, tries 3 times before returning None.

        Returns:
            cursor (object): Cursor object for database.
        """
        if self._cursor == None:
            for i in range(3):
                try:
                    connection = pg8000.connect(
                        user=user,
                        password=password,
                        host=host,
                        port=int(port),
                        database=database,
                    )
                    self._cursor = connection.cursor()

                    # Print PostgreSQL version
                    self._cursor.execute("SELECT version();")
                    record = self._cursor.fetchone()
                    print("You are connected to - ", record, "\n")

                    return self._cursor
                except Exception as error:
                    print(
                        f"Error while connecting to PostgreSQL database.\nTries: {i}\n",
                        error,
                    )

        return self._cursor


def _get_movies_json():
    """
    Returns movies json file if available, else returns None.

    Returns:
        movies_json (dict of str: int): Dictionary mapping movie titles to their respective movie ids (ex: { "Toy Story (1995)": 1, "Jumanji (1995)": 2, ... }).
    """

    try:
        f = open(PATH)

        print(f"SUCCESS: Loaded {PATH}!\n")

        return json.load(f)
    except Exception as e:
        print(e)

        return None


def _create_movies_json(movie_title_to_id_mapping):
    """
    Creates movies json file.

    Args:
        movies_json (dict of str: int): Dictionary mapping movie titles to their respective movie ids (ex: { "Toy Story (1995)": 1, "Jumanji (1995)": 2, ... }).

    Returns:
        None
    """
    try:
        with open(PATH, "w") as outfile:
            json.dump(movie_title_to_id_mapping, outfile)

            print(f"SUCCESS: {PATH} created!\n")
    except Exception as e:
        print(f"ERROR: Failed to create {PATH} - {e}\n")


def _get_all_movies(cursor, movies_json):
    """
    Gets all movies from database.

    Returns:
        movies_json (dict of str: int): Dictionary mapping movie titles to their respective movie ids (ex: { "Toy Story (1995)": 1, "Jumanji (1995)": 2, ... }).
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


DB = _Database()
MOVIES_JSON = _get_movies_json()
MOVIE_TITLE_TO_ID_MAPPING = _get_all_movies(DB.cursor, MOVIES_JSON)

if MOVIES_JSON == None and MOVIE_TITLE_TO_ID_MAPPING != None:
    _create_movies_json(MOVIE_TITLE_TO_ID_MAPPING)
