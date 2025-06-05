"""
Moduł do ładowania i wstępnego przetwarzania danych.
Powinien umożliwiać wczytanie danych z pliku, oraz pobranie go przez url.
Dane powinny być zwracane w formacie pd.DataFrame.
"""
import pandas as pd

def load_retail_data() -> pd.DataFrame:
    """
    Ładuje dane Online Retail II Dataset
    
    Args:
        file_path: Ścieżka do pliku z danymi
        
    Returns:
        DataFrame z danymi retail
    """
    pass


def load_favorita_data() -> pd.DataFrame:
    """
    Ładuje dane Corporación Favorita dataset
    
    Args:
        data_dir: Katalog z plikami danych
        
    Returns:
        Tuple z DataFrames: (train, stores, oil)
    """
    pass

