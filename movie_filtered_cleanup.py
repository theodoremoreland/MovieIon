# %%
import pandas as pd
import csv


# %%
df = pd.read_csv("movie_filtered.csv")

# %%

movielist_df = df.groupby(["movieId"], as_index=False).first()[
    "movieId"].tolist()

# %%
for items in movielist_df:
    print(items)

# %%
movielist_df = pd.DataFrame({
    "movieId": movielist_df
})

# %%
movielist_df.to_csv("movie_list_filtered.csv")
