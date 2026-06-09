import pandas as pd

class DriversOperations:
    def __init__(self, df:pd.DataFrame):
        self.df = df.copy()

    def return_slider_filter(self):
        self.df['dob'] = pd.to_datetime(self.df['dob'], errors='coerce')
        df_clean = self.df.dropna(subset=['dob'])
        df_sorted = df_clean.sort_values(by='dob', ascending=True).reset_index(drop=True)
        min_year = int(df_sorted['dob'].dt.year.iloc[0])
        max_year = int(df_sorted['dob'].dt.year.iloc[-1])
        return min_year, max_year
    
    def get_unique_nationalities(self):
        return sorted(self.df['nationality'].dropna().unique())

    def return_drivers_preformance(self, min_year: int, max_year: int, selected_nationalities: list):
        mask = (self.df['dob'].dt.year >= min_year) & (self.df['dob'].dt.year <= max_year)
        if selected_nationalities:
            mask = mask & (self.df['nationality'].isin(selected_nationalities))
        else:
            return pd.Series(dtype='int64')
    
        df_filtered = self.df[mask]
        return df_filtered['nationality'].value_counts()