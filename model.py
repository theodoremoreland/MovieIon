
#%%
import os
import numpy as np
import pandas as pd

from scipy.sparse import csr_matrix
from sklearn.neighbors import KNeighborsClassifier

from fuzzywuzzy import fuzz

from joblib import load

model_knn = load('knn_model.joblib') 
movie_matrix = load("movie_matrix.joblib")
movie_title_index = load("movie_title_index.joblib")

from sklearn.neighbors import NearestNeighbors
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
model_knn.fit(movie_matrix)


#%%
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
        print('Oops! No match is found')
        return 
    else:
        #print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
        return match_tuple[0][1]


#%%
#Function to make recommendation based on fav_movie or movie choice
def make_recommendation(model_knn, data, fav_movie, mapper, n_recommendations):
    # Choose a movie
    model_knn.fit(data)
    print('You have input movie:', fav_movie)
    # Searching for similar movies
    #print('Recommendation system is looking to find similar movies')
    #print('...............\n')
    # Idx equals the function defined by the similarnamesearch above
    idx = similar_name_search(movie_title_index, fav_movie)
    distances ,indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations+1)
    # get list of raw idx of recommendations
    raw_recommends =         sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    # print recommendations
    #print('Recommendations for {}:'.format(fav_movie))
    movies = []
    distance = []
    for i, (idx, dist) in enumerate(raw_recommends):
        print('{0}: {1}, with distance of {2}'.format(i+1, reverse_mapper[idx], dist))
        #movies.append('{0}: {1}, with distance of {2}'.format(i+1, reverse_mapper[idx], dist))
        movies.append(reverse_mapper[idx])
        distance.append(dist)
    return movies, distance


# my_favorite= "Ghostbust"
# make_recommendation(
#     model_knn=model_knn,
#     data=movie_matrix,
#     fav_movie= my_favorite,
#     mapper=movie_title_index,
#     n_recommendations=10)


#%%



