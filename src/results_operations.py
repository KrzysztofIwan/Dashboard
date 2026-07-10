import pandas as pd

class ResultsOperations:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def get_correlation_data(self, races_df: pd.DataFrame, min_year: int, max_year: int):
        merged_df = self.df.merge(races_df, on='raceId', how='inner')
        merged_df['year'] = pd.to_numeric(merged_df['year'], errors='coerce')
        filtered_df = merged_df[(merged_df['year'] >= min_year) & (merged_df['year'] <= max_year)]
        
        filtered_df['grid'] = pd.to_numeric(filtered_df['grid'], errors='coerce')
        filtered_df['positionOrder'] = pd.to_numeric(filtered_df['positionOrder'], errors='coerce')
        
        return filtered_df[filtered_df['grid'] > 0][['grid', 'positionOrder']].dropna()

    def get_advanced_driver_metrics(self, races_df: pd.DataFrame, drivers_df: pd.DataFrame, min_year: int, max_year: int, selected_nationalities: list):
        df_merged = self.df.merge(races_df, on='raceId').merge(drivers_df, on='driverId')
        
        df_merged['year'] = pd.to_numeric(df_merged['year'], errors='coerce')
        mask = (df_merged['year'] >= min_year) & (df_merged['year'] <= max_year)
        
        if selected_nationalities:
            mask = mask & (df_merged['nationality'].isin(selected_nationalities))
            
        df_filtered = df_merged[mask].copy()
        if df_filtered.empty:
            return pd.DataFrame()
            
        df_filtered['grid'] = pd.to_numeric(df_filtered['grid'], errors='coerce')
        df_filtered['positionOrder'] = pd.to_numeric(df_filtered['positionOrder'], errors='coerce')
        df_filtered['positions_gained'] = df_filtered['grid'] - df_filtered['positionOrder']
        df_filtered['is_soft_finished'] = df_filtered['position'].notna()
        
        driver_stats = df_filtered.groupby(['forename', 'surname']).agg(
            Średni_Awans=('positions_gained', 'mean'),
            Niezawodność=('is_soft_finished', lambda x: round(x.mean() * 100, 1)),
            Liczba_Wyścigów=('raceId', 'count')
        ).reset_index()
        
        driver_stats['Kierowca'] = driver_stats['forename'] + " " + driver_stats['surname']
        return driver_stats[driver_stats['Liczba_Wyścigów'] >= 5][['Kierowca', 'Średni_Awans', 'Niezawodność', 'Liczba_Wyścigów']]

    def get_constructor_dominance(self, races_df: pd.DataFrame, constructors_df: pd.DataFrame, min_year: int, max_year: int):

        df_merged = self.df[['raceId', 'constructorId', 'points']].merge(
            races_df[['raceId', 'year']], on='raceId'
        ).merge(
            constructors_df[['constructorId', 'name']], on='constructorId'
        )
        df_merged.rename(columns={'name': 'Zespol'}, inplace=True)
        df_merged['year'] = pd.to_numeric(df_merged['year'], errors='coerce')
        df_merged['points'] = pd.to_numeric(df_merged['points'], errors='coerce')

        mask = (df_merged['year'] >= min_year) & (df_merged['year'] <= max_year)
        df_filtered = df_merged[mask]

        if df_filtered.empty or df_filtered['points'].sum() == 0:
            return pd.DataFrame()

        total_points = df_filtered['points'].sum()

        dom_df = df_filtered.groupby('Zespol')['points'].sum().reset_index()
        dom_df['Współczynnik_Dominacji'] = (dom_df['points'] / total_points) * 100
        dom_df['Współczynnik_Dominacji'] = dom_df['Współczynnik_Dominacji'].round(2)
        dom_df = dom_df.sort_values(by='Współczynnik_Dominacji', ascending=False)
        
        return dom_df.head(10)