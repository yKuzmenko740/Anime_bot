import pandas as pd
import warnings

warnings.filterwarnings('ignore')


class Preprocessing:

    def __init__(self):
        self.df = pd.DataFrame()

    def get_data(self) -> pd.DataFrame:
        return self.df

    def load_csv(self, main_anime: str, desc: str):
        df = pd.read_csv(main_anime)
        df_desc = pd.read_csv(desc)
        df['sypnopsis'] = df_desc.sypnopsis
        self.df = df

    def preprocess(self):
        # dropping rows with unknown
        unknown_english_ind = self.df[self.df['English name'] == 'Unknown'].index
        self.df.loc[unknown_english_ind, 'English name'] = self.df.loc[unknown_english_ind, 'Name']
        self.df.drop(self.df[self.df.Type == 'Movie'].index, inplace=True)
        # dropping scores columns
        scores = [f"Score-{i}" for i in range(1, 11)]
        self.df.drop(columns=scores, axis=1, inplace=True)
        self.df = self.df.drop(self.df[self.df.Aired == "Unknown"].index)
        self.df.Episodes[self.df.Episodes == 'Unknown'] = 0
        self.df = self.df.drop(self.df[self.df.Episodes.astype('int64') < 3].index)
        self.df.Rating = self.df.Rating.replace({'Unknown': self.df.Rating.mode()[0]})

    def create_soup(self, X: pd.DataFrame):
        return ''.join(X['Genders']) + ' ' + ''.join(X['Type']) + ' ' + X['Aired'] + ' ' + ''.join(
            X['Rating']) + ' ' + ''.join(X['Producers']) + ' ' + ''.join(X['Clear name'])

    def clean_data(self, X):
        if isinstance(X, list):
            return [str.lower(i.replace(" ", "")) for i in X]
        else:
            # Check if director exists. If not, return empty string
            if isinstance(X, str):
                return str.lower(X.replace(" ", ""))
            else:
                return ''

    def get_X(self):
        X = self.df[["English name", "Score", "Genders", "Type", "Aired", "Rating", "Producers", 'sypnopsis']]
        X.Score = X.Score.replace({"Unknown": '-100'}).astype("float64")
        X.Score[X.Score == -100] = X.Score.median()
        X.sypnopsis[X.sypnopsis.isna()] = 'Unknown'
        X.sypnopsis[X.sypnopsis == 'Unknown'] = ''
        X.Genders[X.Genders == "Unknown"] = ''
        X.drop(X.Type[X.Type == "Unknown"].index, inplace=True)
        X.Producers[X.Producers == "Unknown"] = ''
        X['English name'] = X['English name'].drop_duplicates()
        X["Clear name"] = X['English name'].str.replace(" ", "")
        X['Clear name'] = X['Clear name'].str.lower()
        X['sypnopsis'] = X['sypnopsis'].fillna('')
        features = ['Genders', 'Type', 'Aired', 'Rating', 'Producers', 'Clear name']
        for feature in features:
            X[feature] = X[feature].apply(self.clean_data)
        X['soup'] = X.apply(self.create_soup, axis=1)
        return X
