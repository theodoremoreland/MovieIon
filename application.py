# Native library
import ast
import random

# Third party
import pg8000
from flask import (Flask, render_template, request, redirect, session, flash, jsonify)

# Custom
from scripts.model import (make_recommendation, worst_recommendations)
from scripts.model import (model_knn, movie_matrix, movie_title_index)
from scripts.config import (user, password, host, port, database, secret_key)


application = Flask(__name__)
application.config['DEBUG'] = True
application.secret_key = secret_key



@application.before_first_request
def setup():

    global cursor, id_index

    id_index = {"id": [], "title": []}

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


@application.route("/", methods=['POST', 'GET'])
def index():

    global cursor, id_index

    try:
        cursor.execute('SELECT title, movie_id FROM movie_list;')
        all_movies = cursor.fetchall()
        id_index["title"] = [x[0] for x in all_movies]
        id_index["id"] = [x[1] for x in all_movies]

    except (Exception) as error:
        print ("Error while selecting rows(title, movie_id)", error)  
    return render_template("index.html", all_movies=all_movies)


@application.route("/instructions")
def instructions():
    return render_template("instructions.html")


@application.route('/about')
def about():
    return render_template("about.html")


@application.route('/login', methods=['POST', 'GET'])
def login():

    global cursor

    if request.method == 'POST':

        username = request.form['username']
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute(f"SELECT user_id, username, watchlist FROM users WHERE username = '{username}';") # postgres can only interpret single quoted strings
        user_info = cursor.fetchone()
        print(user_info)
        if user_info:
            if user_info[1] == username:
                session['username'] = username
                return redirect(f"/profile/{username}")
            else:
                flash('invalid username')
        else:
            flash('invalid username')
    return render_template('login.html')


@application.route('/logout')
def logout():
    if 'username' in session:
        username = session['username']
        del session['username']
        flash(f"{username} is now logged out")
    else:
        flash("You need to log in before you can log out")
    return redirect("/login")


@application.route('/profile/<username>', methods=['POST', 'GET'])
def render_profile(username):

    global cursor

    if 'username' in session:
        if username == "user":
            username = session['username']
    else:
        return redirect('/login')

    try:
        cursor.execute(f"SELECT watchlist FROM users WHERE username = '{username}';")
        watchlist = cursor.fetchone() # Returns 2d array wherein first and singular element contains actual data.
        movieIDs = []
        for movie in watchlist[0]:
            cursor.execute(f"SELECT movie_id FROM movie_list WHERE title = '{movie}';")
            movieID = cursor.fetchone()[0]
            movieIDs.append(movieID)
        return render_template("profile.html", movieIDs=movieIDs, watchlist=watchlist, username=username)

    except (Exception) as error:
        print ("Error while querying database", error)

    return render_template("profile.html", movieIDs=[[]], watchlist=[[]], username=username) # 2d arrays simulate a null return from queries


@application.route('/info/<movie_id>')
def display_movie_info(movie_id):

    global cursor

    cursor.execute('BEGIN TRANSACTION;')
    cursor.execute(f"SELECT * FROM metadata WHERE id = '{movie_id}';")
    metadata = cursor.fetchone()


    _id = metadata[0]
    title = metadata[1]
    overview = metadata[2]
    crew = ast.literal_eval(metadata[3]) #list of tuples
    cast = ast.literal_eval(metadata[4]) #list
    genres = ast.literal_eval(metadata[5]) #list
    language = metadata[6]
    runtime = metadata[7]
    budget = metadata[8]
    revenue = metadata[9]

    return render_template("info.html", movie_id=movie_id, title=title, overview=overview, crew=crew, cast=cast, genres=genres, language=language, runtime=runtime, budget=budget, revenue=revenue)


@application.route('/watchlist/<movie_id>', methods=['POST', 'GET'])
def add_to_watchlist(movie_id):

    global cursor

    try:
        cursor.execute(f"SELECT title FROM movie_list WHERE movie_id = '{movie_id}';")
        movie = cursor.fetchone()[0]
        movie = movie.replace(",", ",,")
        movie = movie.replace("'", "''")
        username = session["username"]
        cursor.execute('BEGIN TRANSACTION;')
        cursor.execute(f"UPDATE users SET watchlist = array_append(watchlist, '{movie}') WHERE username = '{username}';")
        cursor.execute('COMMIT;')
        cursor.execute(f"SELECT watchlist FROM users WHERE username = '{username}';")
        recently_added_to_watchlist = cursor.fetchone()[0][-1]
        flash(f"{recently_added_to_watchlist} successfully added to watchlist!")
        return redirect(f"/info/{movie_id}")
        
    except (Exception) as error:
        print ("Error while querying database", error)
        flash("There was an error when attempting to add to watchlist!")
        return redirect(f"/info/{movie_id}")


@application.route('/remove/<movie>', methods=['POST', 'GET'])
def remove_from_watchlist(movie):

        global cursor

        movie = movie.replace(",", ",,")
        movie = movie.replace("'", "''")
        try:
            username = session["username"]
            cursor.execute('BEGIN TRANSACTION;')
            cursor.execute(f"UPDATE users SET watchlist = array_remove(watchlist, '{movie}') WHERE username = '{username}';")
            cursor.execute('COMMIT;')
        except (Exception) as error:
            print ("Error while querying database", error)
        return redirect(f'/profile/{username}')


@application.route('/choices', methods=['POST', 'GET'])
def recommend_positive_movies():

    global cursor, id_index

    #(title, dist)
    recommendations1 = []
    recommendations2 = []
    recommendations3 = []

    if request.method == 'POST':
        movies = request.get_json() 
        print(movies)

        recommendations1.append(
        make_recommendation(
            model_knn=model_knn,
            data=movie_matrix,
            fav_movie = movies[0],
            mapper=movie_title_index,
            n_recommendations=10)
        )

        recommendations2.append(
        make_recommendation(
            model_knn=model_knn,
            data=movie_matrix,
            fav_movie = movies[1],
            mapper=movie_title_index,
            n_recommendations=10)
        )

        recommendations3.append(
        make_recommendation(
            model_knn=model_knn,
            data=movie_matrix,
            fav_movie = movies[2],
            mapper=movie_title_index,
            n_recommendations=10)
        )

        #titles
        mix1 = []
        mix2 = []
        mix3 = []

        #dist
        dist1 = []
        dist2 = []
        dist3 = []

        # For each set of recommedations (3), pick a random recommendation and append to "mix" list
        for i in range(3):
            j = str(i + 1)
            recommendations = eval("recommendations" + j)
            mix = eval("mix" + j)
            dist = eval("dist" + j)
            for _ in range(5):
                scramble = random.randint(0, 9)
                while recommendations[0][0][scramble] in mix or recommendations[0][0][scramble] in movies:
                    scramble = random.randint(0, 9)
                mix.append(recommendations[0][0][scramble])
                dist.append(recommendations[0][1][scramble])
        
        list1 = []
        list2 = []
        list3 = []

        for i in range(3):
            j = str(i + 1)
            mix = eval("mix" + j)
            for movie in mix:
                movie = movie.replace(",", "").lower()
                for i, title in enumerate(id_index["title"]):
                    title_l = title.lower()
                    #if movie[-5:] in title and movie[:4] in title:
                        # print ("Comparing '%r' with '%r'" % (movie, title))
                        # print(movie == title)
                    if movie in title_l:
                        movie_id = id_index["id"][i]
                        eval("list" + j).append([title, movie_id])

        return jsonify({'data': render_template('recommended.html',
                                                 list1=list1, 
                                                 list2=list2,
                                                 list3=list3,
                                                 dist1=dist1,
                                                 dist2=dist2,
                                                 dist3=dist3,
                                                 movies=movies)})
    
    return redirect("/")


@application.route('/worst', methods=['POST', 'GET'])
def recommend_negative_movies():

    global cursor, id_index

    
    #(title, dist)
    recommendations1 = []
    recommendations2 = []
    recommendations3 = []

    if request.method == 'POST':
        movies = request.get_json() 
        print(movies)

        recommendations1.append(
        worst_recommendations(
            model_knn=model_knn,
            data=movie_matrix,
            fav_movie = movies[0],
            mapper=movie_title_index,
            n_recommendations=100)
        )

        recommendations2.append(
        worst_recommendations(
            model_knn=model_knn,
            data=movie_matrix,
            fav_movie = movies[1],
            mapper=movie_title_index,
            n_recommendations=100)
        )

        recommendations3.append(
        worst_recommendations(
            model_knn=model_knn,
            data=movie_matrix,
            fav_movie = movies[2],
            mapper=movie_title_index,
            n_recommendations=100)
        )

        #titles
        mix1 = []
        mix2 = []
        mix3 = []

        #dist
        dist1 = []
        dist2 = []
        dist3 = []

        print(recommendations1)
        #for each set of recommedations (3), pick a random recommendation and append to "mix" list
        for i in range(3):
            j = str(i + 1)
            recommendations = eval("recommendations" + j)
            mix = eval("mix" + j)
            dist = eval("dist" + j)
            for _ in range(5):
                scramble = random.randint(0, 9)
                while recommendations[0][0][scramble] in mix or recommendations[0][0][scramble] in movies:
                    scramble = random.randint(0, 9)
                mix.append(recommendations[0][0][scramble])
                dist.append(recommendations[0][1][scramble])
        
        list1 = []
        list2 = []
        list3 = []

        for i in range(3):
            j = str(i + 1)
            mix = eval("mix" + j)
            for movie in mix:
                movie = movie.replace(",", "").lower()
                for i, title in enumerate(id_index["title"]):
                    title_l = title.lower()
                    #if movie[-5:] in title and movie[:4] in title:
                        # print ("Comparing '%r' with '%r'" % (movie, title))
                        # print(movie == title)
                    if movie in title_l:
                        movie_id = id_index["id"][i]
                        eval("list" + j).append([title, movie_id])
        print(list3, dist3)
        return jsonify({'data': render_template('worst.html',
                                                 list1=list1, 
                                                 list2=list2,
                                                 list3=list3,
                                                 dist1=dist1,
                                                 dist2=dist2,
                                                 dist3=dist3,
                                                 movies=movies)})
    
    return redirect("/")



if __name__ == "__main__":
    application.run()
