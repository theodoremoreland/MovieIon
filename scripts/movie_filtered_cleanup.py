# %%
import pandas as pd

# %%
movie_filtered_final_df = pd.read_csv("movie_filtered_final.csv")

# %%
movie_filtered_final_df.drop("Unnamed: 0.1", axis=1, inplace=True)

# %%
movie_filtered_final_df.set_index("movieId", inplace=True)

# %%
