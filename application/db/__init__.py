import pg8000

from modules.config import user, password, host, port, database


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


cursor = database_cursor()


def get_all_movies():
    """
    Gets all movies from database.

    Returns:
        all_movies (list): List of tuples containing movie title and movie id.
        movie_title_to_id_mapping (dict): Dictionary mapping movie titles to their respective movie ids.
    """

    """
    movie_title_to_id_mapping is a dictionary that maps movie titles to their respective movie ids.

    Example: movie_title_to_id_mapping = { "Toy Story (1995)": 1, "Jumanji (1995)": 2, ... }
    """
    movie_title_to_id_mapping = {}

    try:
        cursor.execute("SELECT title, movie_id FROM movie_list;")
        all_movies = cursor.fetchall()

        for _, (movie_title, movie_id) in enumerate(all_movies):
            movie_title_to_id_mapping[movie_title] = movie_id

        # TODO returning both values is redundant. Just return movie_title_to_id_mapping and refactor index.html.
        return [all_movies, movie_title_to_id_mapping]

    except Exception as error:
        print("Error while selecting rows(title, movie_id)", error)


[all_movies, movie_title_to_id_mapping] = get_all_movies()
