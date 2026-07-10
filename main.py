import streamlit as st
import pandas as pd
import plotly.express as px
from src.drivers_operations import DriversOperations
from src.races_operations import RacesOperations
from src.circuits_operations import CircuitsOperations
from src.results_operations import ResultsOperations
from src.constructors_operations import ConstructorsOperations

st.set_page_config(page_title="F1 World Championship", page_icon="🏎️", layout="wide")

@st.cache_data
def load_and_prep_data():
    races = pd.read_csv('data/races.csv').replace(r'\N', pd.NA)
    results = pd.read_csv('data/results.csv').replace(r'\N', pd.NA)
    circuits = pd.read_csv('data/circuits.csv').replace(r'\N', pd.NA)
    drivers = pd.read_csv('data/drivers.csv').replace(r'\N', pd.NA)
    constructors = pd.read_csv('data/constructors.csv').replace(r'\N', pd.NA)
    return races, results, circuits, drivers, constructors

races_df, results_df, circuits_df, drivers_df, constructors_df = load_and_prep_data()

races_operations = RacesOperations(races_df)
result_operations = ResultsOperations(results_df)
circuits_operations = CircuitsOperations(circuits_df)
drivers_operations = DriversOperations(drivers_df)
constructors_operations = ConstructorsOperations(constructors_df)

driver_yob_first, driver_yob_last = drivers_operations.return_slider_filter()
race_year_first, race_year_last = races_operations.return_slider_filter()
all_nationalities = drivers_operations.get_unique_nationalities()
all_circuits = circuits_df['name'].unique().tolist()
all_constructors = constructors_operations.get_unique_constructors()

st.sidebar.title("Panel filtrowania")
st.sidebar.header("Filtry wyścigów")
selected_year_race = st.sidebar.slider("Wybierz zakres lat wyścigów", race_year_first, race_year_last, (race_year_first, race_year_last))
selected_circuits = st.sidebar.multiselect("Wybierz tor wyścigowy", options=all_circuits, default=all_circuits[:5])

st.sidebar.markdown("---")
st.sidebar.header("Filtry kierowców")
selected_yob_drivers = st.sidebar.slider("Wybierz rok urodzenia kierowcy", driver_yob_first, driver_yob_last, (driver_yob_first, driver_yob_last))
selected_nationalities = st.sidebar.multiselect("Wybierz narodowość", options=all_nationalities, default=all_nationalities[:3])

st.sidebar.markdown("---")
st.sidebar.header("Filtry Zespołów")
selected_constructors = st.sidebar.multiselect("Wybierz zespoły", options=all_constructors, default=all_constructors[:5])

races_df['year'] = pd.to_numeric(races_df['year'], errors='coerce')
filtered_races = races_df[(races_df['year'] >= selected_year_race[0]) & (races_df['year'] <= selected_year_race[1])]
filtered_results = results_df[results_df['raceId'].isin(filtered_races['raceId'])]

if selected_circuits:
    filtered_circuits = circuits_df[circuits_df['name'].isin(selected_circuits)]
else:
    filtered_circuits = pd.DataFrame()

drivers_df['dob'] = pd.to_datetime(drivers_df['dob'], errors='coerce')
mask_drivers = (drivers_df['dob'].dt.year >= selected_yob_drivers[0]) & (drivers_df['dob'].dt.year <= selected_yob_drivers[1])
if selected_nationalities:
    mask_drivers = mask_drivers & drivers_df['nationality'].isin(selected_nationalities)
filtered_drivers = drivers_df[mask_drivers]

if selected_constructors:
    filtered_constructors = constructors_df[constructors_df['name'].isin(selected_constructors)]
else:
    filtered_constructors = pd.DataFrame()

st.title(f"Analiza wyścigów F1 (lata {race_year_first} - {race_year_last})")
st.header("Metryki zbiorów danych (przefiltrowane)")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Wyścigi", filtered_races.shape[0], border=True)
col2.metric("Wyniki wyścigów", filtered_results.shape[0], border=True)
col3.metric("Tory wyścigowe", filtered_circuits.shape[0], border=True)
col4.metric("Kierowcy", filtered_drivers.shape[0], border=True)
col5.metric("Zespoły", filtered_constructors.shape[0], border=True)
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Kierowcy i Zespoły", "Analiza Przestrzenna", "Zaawansowane Statystyki"])

with tab1:
    st.header("Demografia i profil kierowców")
    driver_country = drivers_operations.return_drivers_performance(
        min_year=selected_yob_drivers[0],
        max_year=selected_yob_drivers[1],
        selected_nationalities=selected_nationalities
    )
    
    if not driver_country.empty:
        st.bar_chart(driver_country)
        
        csv = driver_country.to_csv().encode('utf-8')
        st.download_button(
            label="Pobierz dane jako CSV",
            data=csv,
            file_name='kierowcy_statystyki.csv',
            mime='text/csv',
        )
        
        with st.expander("Komentarz analityczny"):
            st.write("Wykres obrazuje dominację wybranych narodowości w Formule 1. Opcja pobrania umożliwia dalszą analizę struktury demograficznej w zewnętrznych narzędziach.")
    else:
        st.info("Brak kierowców spełniających wybrane kryteria.")

    st.markdown("---")
    st.header("Dominacja Zespołów")
    
    constructor_dom = constructors_operations.get_constructor_dominance(
        results_df, races_df, selected_year_race[0], selected_year_race[1], selected_constructors
    )
    
    if not constructor_dom.empty:
        fig_bar = px.bar(
            constructor_dom, 
            x="Zespol", 
            y="Współczynnik_Dominacji",
            title="Udział punktowy wybranych zespołów w puli wszystkich punktów",
            labels={'Zespol': 'Zespół', 'Współczynnik_Dominacji': 'Współczynnik Dominacji (%)'},
            color="Współczynnik_Dominacji",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_bar, width='stretch')
        
        with st.expander("Komentarz analityczny"):
            st.write("Współczynnik dominacji wskazuje, jaki procent wszystkich punktów zdobytych w wybranym przedziale czasowym przypadł danemu zespołowi. Wykorzystanie relacji do tabeli konstruktorów pozwala łatwo zidentyfikować ery dominacji konkretnych stajni wyścigowych.")
    else:
        st.info("Brak wystarczających danych do obliczenia współczynnika dominacji dla wybranych kryteriów.")

with tab2:
    st.header("Lokalizacje torów na świecie")
    map_data = circuits_operations.get_map_data(selected_circuits)
    if not map_data.empty:
        st.map(map_data, zoom=1, width='stretch')
        with st.expander("Komentarz analityczny"):
            st.write("Zagęszczenie torów w Europie historycznie odzwierciedla korzenie tego sportu. Filtracja w panelu bocznym pozwala wyizolować konkretne obiekty i zweryfikować ich szerokość geografizną.")
    else:
        st.info("Wybierz tory w panelu bocznym, aby wyświetlić mapę.")

with tab3:
    st.header("Analiza Efektywności i Niezawodności Kierowców")
    
    adv_metrics = result_operations.get_advanced_driver_metrics(
        races_df, drivers_df, selected_year_race[0], selected_year_race[1], selected_nationalities
    )
    
    if not adv_metrics.empty:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Zestawienie zbiorcze")
            st.dataframe(adv_metrics.sort_values(by="Średni_Awans", ascending=False), width='stretch', hide_index=True)
            
        with col_right:
            st.subheader("Mapa efektywności")
            fig_scatter = px.scatter(
                adv_metrics, x="Niezawodność", y="Średni_Awans",
                text="Kierowca", size="Liczba_Wyścigów",
                labels={'Niezawodność': 'Niezawodność (% ukończonych)', 'Średni_Awans': 'Średni indeks awansu (pozycje)'},
                title="Zależność między niezawodnością a tempem nadrabiania pozycji"
            )
            fig_scatter.update_traces(textposition='top center')
            st.plotly_chart(fig_scatter, width='stretch')
            
        with st.expander("Komentarz analityczny do nowych metryk"):
            st.write("Wysoka wartość indeksu awansu świadczy o doskonałych umiejętnościach wyprzedzania lub słabszych występach w kwalifikacjach wymuszających nadrabianie pozycji. Wskaźnik niezawodności pozwala odróżnić kierowców jeżdżących stabilnie od tych, którzy często nie kończą rywalizacji.")
    else:
        st.info("Brak wystarczających danych dla wybranych filtrów kierowców i wyścigów.")
        
    st.markdown("---")
    st.header("Korelacja: Kwalifikacje a Wyścig")
    corr_data = result_operations.get_correlation_data(races_df, selected_year_race[0], selected_year_race[1])
    
    if not corr_data.empty:
        fig = px.density_heatmap(
            corr_data, x="grid", y="positionOrder",
            title="Heatmapa: Pozycja startowa vs Pozycja końcowa",
            labels={'grid': 'Pozycja startowa', 'positionOrder': 'Miejsce na mecie'},
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("Brak danych do analizy heatmapy korelacji.")