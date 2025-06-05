# Instrukcje pobierania danych

## 1. Online Retail II Dataset

**Źródło:** UCI Machine Learning Repository
**Link:** https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

### Instrukcje pobierania:

1. Przejdź na stronę UCI ML Repository
2. Pobierz plik `online_retail_II.xlsx`
3. Zapisz w folderze `data/raw/`
4. Opcjonalnie przekonwertuj na CSV dla szybszego ładowania

### Opis danych:

- **InvoiceNo:** Numer faktury (6-cyfrowy, zaczyna się od 'C' dla anulowanych)
- **StockCode:** Kod produktu (5-cyfrowy)
- **Description:** Nazwa produktu
- **Quantity:** Ilość każdego produktu na transakcję
- **InvoiceDate:** Data i czas faktury
- **UnitPrice:** Cena jednostkowa
- **CustomerID:** Unikalny identyfikator klienta (5-cyfrowy)
- **Country:** Nazwa kraju gdzie mieszka klient

---

## 2. Corporación Favorita Grocery Sales Forecasting

**Źródło:** Kaggle Competition
**Link:** https://www.kaggle.com/competitions/favorita-grocery-sales-forecasting

### Instrukcje pobierania:

1. Utwórz konto na Kaggle.com
2. Przejdź do konkursu "Favorita Grocery Sales Forecasting"
3. Pobierz następujące pliki:

   - `train.csv` - dane treningowe sprzedaży
   - `test.csv` - dane testowe
   - `stores.csv` - metadane sklepów
   - `oil.csv` - ceny ropy (wpływ na gospodarkę)
   - `holidays_events.csv` - święta i wydarzenia
   - `items.csv` - metadane produktów
   - `transactions.csv` - liczba transakcji

4. Zapisz wszystkie pliki w folderze `data/raw/`

### Opis głównych plików:

#### train.csv

- **date:** Data
- **store_nbr:** Identyfikator sklepu
- **family:** Rodzina produktów
- **sales:** Sprzedaż w danym dniu (cel predykcji)
- **onpromotion:** Liczba elementów w promocji

#### stores.csv

- **store_nbr:** Identyfikator sklepu
- **city:** Miasto
- **state:** Stan
- **type:** Typ sklepu
- **cluster:** Klaster sklepu

#### oil.csv

- **date:** Data
- **dcoilwtico:** Dzienna cena ropy

---

## Alternatywne źródła danych

Jeśli powyższe dane nie są dostępne, można użyć:

1. **Retail Sales Dataset** - dane sprzedażowe z różnych źródeł
2. **Walmart Sales Data** - dane z Kaggle
3. **Rossmann Store Sales** - dane z Kaggle
4. **Store Item Demand Forecasting** - dane z Kaggle

---

## Struktura folderów po pobraniu danych:

```
data/
├── raw/
│   ├── online_retail_II.csv
│   ├── train.csv
│   ├── stores.csv
│   ├── oil.csv
│   ├── holidays_events.csv
│   ├── items.csv
│   └── transactions.csv
└── processed/
    └── (pliki wygenerowane przez skrypty preprocessing)
```
