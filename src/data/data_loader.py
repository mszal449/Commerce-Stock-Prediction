"""
Moduł do ładowania i wstępnego przetwarzania danych.
Powinien umożliwiać wczytanie danych z pliku, oraz pobranie go przez url.
Dane powinny być zwracane w formacie pd.DataFrame.
"""
import pandas as pd
import subprocess
import os
from pathlib import Path


def download_dataset(competition_name: str = "store-sales-time-series-forecasting", 
                     download_path: str = "") -> str:
    """Pobiera dataset z Kaggle Competition"""
    if download_path is None:
        download_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    else:
        download_dir = Path(download_path)
    
    download_dir.mkdir(parents=True, exist_ok=True)
    
    subprocess.run([
        "kaggle", "competitions", "download", 
        "-c", competition_name,
        "-p", str(download_dir)
    ], check=True)
    
    return str(download_dir)

