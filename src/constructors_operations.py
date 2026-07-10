import pandas as pd

class ConstructorsOperations:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def get_unique_constructors(self):
        return sorted(self.df['name'].dropna().unique())

    def get_constructor_dominance(self, results_df: pd.DataFrame, races_df: pd.DataFrame, min_year: int, max_year: int, selected_constructors: list):
        df_merged = results_df[['raceId', 'constructorId', 'points']].merge(
            races_df[['raceId', 'year']], on='raceId'
        ).merge(
            self.df[['constructorId', 'name']], on='constructorId'
        )
        
        df_merged.rename(columns={'name': 'Zespol'}, inplace=True)
        df_merged['year'] = pd.to_numeric(df_merged['year'], errors='coerce')
        df_merged['points'] = pd.to_numeric(df_merged['points'], errors='coerce')
        mask = (df_merged['year'] >= min_year) & (df_merged['year'] <= max_year)
        
        if selected_constructors:
            mask = mask & (df_merged['Zespol'].isin(selected_constructors))
            
        df_filtered = df_merged[mask]

        if df_filtered.empty or df_filtered['points'].sum() == 0:
            return pd.DataFrame()

        total_points = df_filtered['points'].sum()
        dom_df = df_filtered.groupby('Zespol')['points'].sum().reset_index()
        dom_df['Współczynnik_Dominacji'] = (dom_df['points'] / total_points) * 100
        dom_df['Współczynnik_Dominacji'] = dom_df['Współczynnik_Dominacji'].round(2)
        
        return dom_df.sort_values(by='Współczynnik_Dominacji', ascending=False)