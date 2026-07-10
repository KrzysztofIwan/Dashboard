# F1 Analytics Dashboard

## Opis projektu
Dashboard analityczny prezentujący szczegółowe informacje na temat wyścigów Formuły 1 z lat 1950 do 2024. Aplikacja umożliwia wielowymiarową eksplorację danych historycznych, analizę skuteczności kierowców i zespołów oraz wizualizację trendów za pomocą interaktywnych wykresów i map. 

DataSet został pobrany z platformy [Kaggle](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020?resource=download).

### Kluczowe funkcjonalności
* Dynamiczne filtrowanie danych na poziomie całej aplikacji (możliwość zmiany zakresu lat, torów wyścigowych oraz parametrów demograficznych kierowców).
* Modułowa architektura kodu oparta na programowaniu obiektowym (OOP), optymalizująca procesy ETL (Ekstrakcja, Transformacja, Ładowanie) i blendowanie danych.
* Interaktywne wskaźniki KPI aktualizujące się w czasie rzeczywistym na podstawie zadanych kryteriów.
* Prezentacja lokalizacji torów wyścigowych na mapie świata w oparciu o ich współrzędne geograficzne.
* Możliwość eksportowania przefiltrowanych statystyk demograficznych kierowców do plików `.csv`.

### Zaimplementowane metryki analityczne
* **Indeks Awansu:** Obliczona wartość określająca średnią liczbę pozycji zyskanych lub straconych w wyścigu w odniesieniu do miejsca startowego.
* **Wskaźnik Niezawodności:** Procentowy udział wyścigów ukończonych (sklasyfikowanych) w zestawieniu ze wszystkimi startami, pozwalający na ewaluację stabilności kierowcy i sprzętu.
* **Współczynnik Dominacji:** Miara ukazująca procentowy udział zespołu w całkowitej puli punktów zdobytych w wybranym przedziale czasowym, pozwalająca obiektywnie porównywać osiągnięcia zespołów z różnych dekad pomimo zmieniających się systemów punktacji.
* **Heatmapa Korelacji:** Wielowymiarowa analiza badająca siłę korelacji między pozycją wywalczoną w kwalifikacjach a miejscem na mecie.

## Użyte technologie
* Python 3.13.5 - język bazowy do implementacji logiki
* streamlit 1.56.0 - frontend aplikacji i komponenty interaktywne
* pandas 2.3.3 - przygotowanie, inżynieria i obróbka relacyjnej bazy danych
* plotly 5.24.0 - renderowanie zaawansowanych wizualizacji analitycznych (scatter plots, donut charts, heatmaps)

## Uruchomienie
Zainstalowanie wszystkich potrzebnych bibliotek:
```bash
pip install -r requirements.txt
```
Uruchomienie projektu z terminala 
```bash
streamlit run main.py
```