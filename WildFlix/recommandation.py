import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "films_clean2.csv"))

df[["Genre_1", "Genre_2", "Genre_3", "Actors_1", "plot_clean", "imdbRating", "imdbVotes"]] = df[["Genre_1", "Genre_2", "Genre_3", "Actors_1", "plot_clean", "imdbRating", "imdbVotes"]].fillna("")

df["soup"] = (df["Genre_1"] + " " + df["Genre_1"] + " " + df["Genre_2"] + " " + df["Genre_2"] + " " + df["Genre_3"] + " "
            + df["Actors_1"] + " "
            + df["plot_clean"] + " "
            + df["imdbRating"].astype(str) + " "
            + df["imdbVotes"].astype(str))

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df["soup"])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommander(titre):
    idx = df[df["Title"] == titre].index[0]
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    scores = scores[1:6]
    indices = [i[0] for i in scores]
    return df["Title"].iloc[indices]