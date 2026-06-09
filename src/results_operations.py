import pandas as pd

class ResultsOperations:
    def __init__(self, df:pd.DataFrame):
        self.df = df.copy()