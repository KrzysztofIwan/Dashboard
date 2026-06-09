import streamlit as st
import pandas as pd
from src.drivers_operations import DriversOperations
from src.races_operations import RacesOperations
from src.circuits_operations import CircuitsOperations
from src.results_operations import ResultsOperations

st.set_page_config(page_title="F1 World Championship", page_icon="🏎️", layout="wide")

@st.cache_data
def load_and_prep_data():
    #Odczytanie oraz przygotowanie danych - dodanie pustych wartości
    races = pd.read_csv('data/races.csv').replace(r'\N', pd.NA)
    results = pd.read_csv('data/results.csv').replace(r'\N', pd.NA)
    circuits = pd.read_csv('data/circuits.csv').replace(r'\N', pd.NA)
    drivers = pd.read_csv('data/drivers.csv').replace(r'\N', pd.NA)
    return races, results, circuits, drivers

races_df, results_df, circuits_df, drivers_df = load_and_prep_data()

races_operations = RacesOperations(races_df)
result_operations = ResultsOperations(results_df)
circuits_operations = CircuitsOperations(circuits_df)
drivers_operations = DriversOperations(drivers_df)

driver_yob_first, driver_yob_last = drivers_operations.return_slider_filter()
race_year_first, race_year_last = races_operations.return_slider_filter()
all_nationalities = drivers_operations.get_unique_nationalities()

#SIDEBAR
st.sidebar.title("Panel filtrowania")
st.sidebar.header("Filtry wyścigów")
selected_year_race = st.sidebar.slider("Wybierz zakres lat", race_year_first, race_year_last, (race_year_first, race_year_last))
st.sidebar.space(size="xxsmall")
st.sidebar.header("Filtry kierowców")
selected_yob_drivers = st.sidebar.slider("Wybierz rok urodzenia kierowcy",driver_yob_first, driver_yob_last, (driver_yob_first,driver_yob_last))
selected_nationalities = st.sidebar.multiselect("Wybierz narodowść", options=all_nationalities, default=all_nationalities[:3])

#MAINPAGE
st.title(f"Analiza wyścigów F1 na lata od {race_year_first} do {race_year_last}")
st.header("Liczba rekordów w poszczególnych zbiorach")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Wyścigi", races_df.shape[0], border=True)
col2.metric("Wyniki wyścigów", results_df.shape[0], border=True)
col3.metric("Tory wyścigowe", circuits_df.shape[0], border=True)
col4.metric("Kierowcy", drivers_df.shape[0], border=True)
st.markdown("---")
st.title("Kierowcy")
st.header("Wykres narodowości kierowców")

driver_country = drivers_operations.return_drivers_preformance(
    min_year=selected_yob_drivers[0],
    max_year=selected_yob_drivers[1],
    selected_nationalities=selected_nationalities
)
if not driver_country.empty:
    st.bar_chart(driver_country)
else:
    if len(selected_nationalities) == 0:
        st.info("Brak wybranej narodowości dla kierowców kierowców.")
    else:
        st.info("Brak kierowców urodzonych w wybranym przedziale czasowym.")
