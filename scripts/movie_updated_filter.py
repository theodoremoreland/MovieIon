# %%
import pandas as pd
import re

# %%
movie_filter = pd.read_csv("movie_list_filtered.csv")

link_list = pd.read_csv("links.csv")

movie_list = pd.read_csv("movie_updated.csv")

# %%
movie_df = movie_filter.merge(movie_list, on="movieId")

link_df = movie_filter.merge(link_list, on="movieId")
# %%
print(movie_df.head())

# %%
movie_df["year"] = movie_df["title"].apply(
    lambda x: re.search(r"(?!\()\d{4}(?=\))", x).group()
)
# %%

# for items in movie_list["year"]:
#     movie_list["year"] = items.group()

# %%
print(movie_df.count())

# %%
movie_df.to_csv("movie_filtered_final.csv")

link_df.to_csv("link_filtered_final.csv")
