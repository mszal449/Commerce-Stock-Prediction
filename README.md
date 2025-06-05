# Projekt NN - Prognozowanie Popytu na Produkty w Handlu

## Opis projektu

Projekt bada zastosowanie sieci neuronowych jako rozwiązania do prognozowania popytu na produkty w handlu. Kluczowym celem jest odpowiedzenie na pytanie, czy modele neuronowe – od prostych sieci gęstych (MLP) po bardziej zaawansowane jak LSTM – mogą skutecznie przewidywać zapotrzebowanie na towary i tym samym wspierać optymalizację kosztów związanych z zaopatrzeniem i stanami magazynowymi.

## Struktura projektu

```
project/
├── data/                       # Dane surowe i przetworzone
├── notebooks/                  # Jupyter notebooks do eksploracji i analizy
├── src/                       # Kod źródłowy
│   ├── data/                  # Moduły do przetwarzania danych
│   ├── models/                # Implementacje modeli
│   ├── evaluation/            # Metryki i ewaluacja
│   └── utils/                 # Funkcje pomocnicze
├── results/                   # Wyniki eksperymentów
├── config/                    # Pliki konfiguracyjne
└── requirements.txt           # Zależności
```

## Wykorzystywane dane

1. **Online Retail II Dataset** (UCI ML Repository)

   - Transakcje w sklepie internetowym z Wielkiej Brytanii (2009-2011)
   - Zawiera: datę transakcji, ilość produktów, kraj, ID klienta, opisy produktów

2. **Corporación Favorita Grocery Sales Forecasting**
   - Ponad 3 miliony rekordów dziennych danych sprzedażowych
   - 54 sklepy, 33 rodziny produktów
   - Zawiera: sprzedaż jednostkową, promocje, metadane sklepów, kategorie produktów

## Modele do przetestowania

- Model bazowy: Regresja liniowa / Prophet
- Sieć gęsta (MLP)
- LSTM (Long Short-Term Memory)

## Metryki ewaluacji

- MAE (Mean Absolute Error)
- RMSE (Root Mean Square Error)
- Wizualna analiza jakości predykcji
