# Note: joblib models can only be used by the same version of joblib, sklearn, scikit-learn that created them.
# Note: Certain versions of joblib, sklearn, scikit-learn are not available on newer versions of python.
# Note: Certain versions of joblib, sklearn, scikit-learn are not compatible with each other not this codebase.
# Note: The requirements.txt file contains the last versions of joblib, sklearn, scikit-learn that are compatible with each other and this codebase.
# Note: As of this writing, Python 3.9 and above are not compatible with versions listed in requirements.txt.

# %%
from joblib import dump, load
from sklearn.neighbors import NearestNeighbors
import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import KNeighborsClassifier

from fuzzywuzzy import fuzz
import pickle


# %%
# File Path
movies_file = "movies.csv"
ratings_file = "ratings.csv"
# Read in the Data
movies_df = pd.read_csv("movies.csv")
ratings_df = pd.read_csv("ratings.csv")


# %%
ratings_file = "ratings.csv"
ratings_df = pd.read_csv(ratings_file)


# %%
movies_df.head()


# %%
movies_df.info()


# %%
ratings_df.head()


# %%
ratings_df.info()


# %%
number_users = len(ratings_df.userId.unique())
number_movies = len(ratings_df.movieId.unique())
print(
    "There are {} users and {} movies in this dataset.".format(
        number_users, number_movies
    )
)


# %%
# get rating frequency of movies
movie_ratings_count = pd.DataFrame(
    ratings_df.groupby("movieId").size(), columns=["count"]
)
movie_ratings_count.sort_values("count", ascending=False).head()


# %%
movie_ratings_count["count"].quantile(np.arange(1, 0.0, -0.1))


# %%
# filter data by count of reviews
number_reviews = 75
popular_movies = list(set(movie_ratings_count.query("count >= @number_reviews").index))
filtered_movie_df = ratings_df[ratings_df.movieId.isin(popular_movies)]
filtered_movie_df.info()


# %%
# get ratings frequency of users
user_ratings_count = pd.DataFrame(
    filtered_movie_df.groupby("userId").size(), columns=["count"]
)
user_ratings_count.sort_values("count", ascending=False).head()


# %%
user_ratings_count["count"].quantile(np.arange(1, 0.0, -0.10))


# %%
# filter data by count of user ratings
user_reviews = 210
popular_users = list(set(movie_ratings_count.query("count >= @user_reviews").index))
filtered_user_df = filtered_movie_df[filtered_movie_df.movieId.isin(popular_users)]
filtered_user_df.info()


# %%
filtered_user_df.head(15)


# %%
# Merging Dataset
movie_ratings_df = pd.merge(filtered_user_df, movies_df, on="movieId")
movie_ratings_df.head()


# %%
# Export file as a CSV
# movie_ratings_df.to_csv("movie_filtered.csv", index=False, header=True)


# %%
# Determining the number of unique users and movies in the filtered down database
number_users = len(movie_ratings_df.userId.unique())
number_movies = len(movie_ratings_df.movieId.unique())
print(
    "There are {} users and {} movies in this dataset.".format(
        number_users, number_movies
    )
)


# %%
# Pivoting the dataframe
df_movie_pivot = filtered_user_df.pivot(
    index="movieId", columns="userId", values="rating"
).fillna(0)


# %%
# creating movie name index
movie_title_index = {
    movie: i
    for i, movie in enumerate(
        list(movies_df.set_index("movieId").loc[df_movie_pivot.index].title)
    )
}

# convert dataframe of movie features to scipy sparse matrix
movie_matrix = csr_matrix(df_movie_pivot.values)


# %%
print(movie_title_index)


# %%
model_knn = NearestNeighbors(
    metric="cosine", algorithm="brute", n_neighbors=20, n_jobs=-1
)
model_knn.fit(movie_matrix)


# %%
type(model_knn)


# %%
dump(model_knn, "knn_model.joblib")


# %%
model_knn = load("knn_model.joblib")


# %%

dump(movie_title_index, "movie_title_index.joblib")


# %%
movie_title_index = load("movie_title_index.joblib")


# %%
dump(movie_matrix, "movie_matrix.joblib")


# %%
movie_matrix = load("movie_matrix.joblib")


# %%
def similar_name_search(mapper, fav_movie):
    match_tuple = []
    # Get a match between user movie choice and titles in the database
    for title, idx in movie_title_index.items():
        ratio = fuzz.ratio(str(title).lower(), str(fav_movie).lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    # Sort the possible matches and see if they match up with the tuple
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        print("Oops! No match is found")
        return
    else:
        print(
            "Found possible matches in our database: {0}\n".format(
                [x[0] for x in match_tuple]
            )
        )
        return match_tuple[0][1]


# %%
# Function to make recommendation based on fav_movie or movie choice
def make_recommendation(model_knn, data, fav_movie, mapper, n_recommendations):
    # Choose a movie
    model_knn.fit(data)
    print("You have input movie:", fav_movie)
    # Searching for similar movies
    print("Recommendation system is looking to find similar movies")
    print("...............\n")
    # Idx equals the function defined by the similarnamesearch above
    idx = similar_name_search(movie_title_index, fav_movie)
    distances, indices = model_knn.kneighbors(
        data[idx], n_neighbors=n_recommendations + 1
    )
    # get list of raw idx of recommendations
    raw_recommends = sorted(
        list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
        key=lambda x: x[1],
    )[:-1:0]
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    # print recommendations
    print("Recommendations for {}:".format(fav_movie))
    for i, (idx, dist) in enumerate(raw_recommends):
        print("{0}: {1}, with distance of {2}".format(i + 1, reverse_mapper[idx], dist))


# %%
my_favorite = "Toy Story"

make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
my_favorite = "Ghostbust"

make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
my_favorite = "Back to the future"

make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
my_favorite = "little women"

make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
my_favorite = "pretty woman"

make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
my_favorite = "i am sam"

make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
my_favorite = "legally blonde"

make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
my_favorite = "my big fat greek wedding"

make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
my_favorite = "isle of dogs"

make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
my_favorite = "pitch perfect"

make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
my_favorite = "ghost"
make_recommendation(
    model_knn=model_knn,
    data=movie_matrix,
    fav_movie=my_favorite,
    mapper=movie_title_index,
    n_recommendations=10,
)


# %%
