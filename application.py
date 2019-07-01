import random
import pg8000
from flask import (Flask, render_template, request, redirect, session, flash, jsonify)
from config import (user, password, host, port, database, secret_key)
from model import make_recommendation
from model import (model_knn, movie_matrix, movie_title_index)



application = Flask(__name__)
# Remember to change this when deploying
application.config['DEBUG'] = True
application.secret_key = secret_key

# @application.before_first_request
# def setup():




id_index = {"id": [], "title": []}
@application.route("/", methods=['POST', 'GET'])
def index():

    try:
        connection = pg8000.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=int(port),
                                    database=database)
        
        cursor = connection.cursor()

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception) as error:
        print ("Error while connecting to PostgreSQL database", error)
        connection = pg8000.connect(user = user,
                                password = password,
                                host = host,
                                port = int(port),
                                database = database)

        cursor = connection.cursor()

    try:
        cursor.execute('SELECT title, movie_id FROM movie_list;')
        all_movies = cursor.fetchall()
        id_index["title"] = [x[0] for x in all_movies]
        id_index["id"] = [x[1] for x in all_movies]
        # print(id_index["title"])
        # print(id_index["id"])
    except (Exception) as error:
        print ("Error while selecting rows(title, movie_id)", error)  
    return render_template("index.html", all_movies=all_movies)


@application.route('/choices', methods=['POST', 'GET'])
def choices():

    recommendations = []

    if request.method == 'POST':
        movies = request.get_json() 
        print(movies)

        recommendations.append(
        make_recommendation(
            model_knn=model_knn,
            data=movie_matrix,
            fav_movie = movies[0],
            mapper=movie_title_index,
            n_recommendations=10)
        )

        recommendations.append(
        make_recommendation(
            model_knn=model_knn,
            data=movie_matrix,
            fav_movie = movies[1],
            mapper=movie_title_index,
            n_recommendations=10)
        )

        recommendations.append(
        make_recommendation(
            model_knn=model_knn,
            data=movie_matrix,
            fav_movie = movies[2],
            mapper=movie_title_index,
            n_recommendations=10)
        )

        mix = []
        for i in range(3):
            for x in range(5):
                scramble = random.randint(0, 9)
                while recommendations[i][scramble] in mix:
                    scramble = random.randint(0, 9)
                mix.append(recommendations[i][scramble])
        
        mix2 = []
        test = ['Blue Angel, The (Blaue Engel, Der) (1930)',
                'War Room, The (1993)',
                'Fast, Cheap & Out of Control (1997)']

        for movie in mix:
            movie = movie.replace(",", "").lower()
            for i, title in enumerate(id_index["title"]):
                title_l = title.lower()
                #if movie[-5:] in title and movie[:4] in title:
                    # print ("Comparing '%r' with '%r'" % (movie, title))
                    # print(movie == title)
                if movie in title_l:
                    movie_id = id_index["id"][i]
                    mix2.append([title, movie_id])
        print(mix2)
        return jsonify({'data': render_template('recommended.html', mix=mix2)})
    
    return redirect("/")



if __name__ == "__main__":
    application.run()
