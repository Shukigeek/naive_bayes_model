import pandas as pd

class Model:
    def __init__(self, df: pd.DataFrame, classified: str):
        self._validate_input(df, classified)
        self.df = df
        self.classified = classified
        self.features = self._get_features()
        self.labels = self._get_labels()
        self.model = {}

    def _validate_input(self, df: pd.DataFrame, classified: str):
        if df is None or df.empty:
            raise ValueError("Received empty DataFrame.")
        if classified not in df.columns:
            raise ValueError(f"Column '{classified}' not found in DataFrame.")

    def _get_features(self):
        return [col for col in self.df.columns if col != self.classified]

    def _get_labels(self):
        return self.df[self.classified].unique()

    def create_model(self):
        for column in self.features:
            self.model[column] = {}
            size = len(self.df[column].unique())
            for val in self.df[column].unique():
                self.model[column][val] = {}
                for label in self.labels:
                    clas = self.df[self.df[self.classified] == label]
                    self.model[column][val][label] = (len(clas[clas[column] == val])+1) / (len(clas) + size)
