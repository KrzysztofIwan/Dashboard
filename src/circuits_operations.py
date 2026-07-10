import pandas as pd

class CircuitsOperations:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def get_map_data(self, selected_circuits: list):
        df = self.df.copy()
        if selected_circuits:
            df = df[df['name'].isin(selected_circuits)]
            
        # Konwersja do typów zmiennoprzecinkowych z obsługą błędów
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lng'], errors='coerce') 
        
        return df[['name', 'location', 'country', 'lat', 'lon']].dropna()