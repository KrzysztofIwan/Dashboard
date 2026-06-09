import pandas as pd

class RacesOperations:
    def __init__(self, df:pd.DataFrame):
        self.df = df.copy()

    def return_slider_filter(self):
        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        df_clean = self.df.dropna(subset=['date'])
        df_sorted = df_clean.sort_values(by='date', ascending=True).reset_index(drop=True)
        min_year = int(df_sorted['date'].dt.year.iloc[0])
        max_year = int(df_sorted['date'].dt.year.iloc[-1])
        return min_year, max_year