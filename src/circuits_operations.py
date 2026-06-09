import pandas as pd

class CircuitsOperations:
    def __init__(self, df:pd.DataFrame):
        self.df = df.copy()