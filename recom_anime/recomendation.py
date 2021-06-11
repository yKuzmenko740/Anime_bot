import numpy as np
import pandas as pd
import numpy
import warnings

warnings.filterwarnings('ignore')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommend:

    def __init__(self):
        self.cosine_sim = None
        self.X = None
        self.indices = None

    @staticmethod
    def get_recommendations(name, X, cosine_sim, indeces):
        idx = indeces[name]
        # Get the pairwsie similarity scores of all animes with that anime
        sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:10]

        movie_indices = [i[0] for i in sim_scores]

        return X["English name"].iloc[movie_indices]

    def preprocess(self, X):
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(X['soup'])
        self.cosine_sim = cosine_similarity(count_matrix, count_matrix)
        indexes = X['English name'].str.replace(" ", "")
        indexes = indexes.str.lower()
        self.X = X.reset_index()
        self.indices = pd.Series(self.X.index, index=indexes).drop_duplicates()

    def get_predictions(self, X, name):
        self.preprocess(X)
        name = name.lower().replace(" ", "")
        return Recommend.get_recommendations(name, self.X, self.cosine_sim, self.indices)
