#!/usr/bin/env python3
"""
Główny skrypt do uruchomienia eksperymentów prognozowania popytu

Użycie:
    python main.py --experiment [data_exploration|preprocessing|baseline|neural_networks|comparison]
    python main.py --experiment all  # uruchomienie wszystkich eksperymentów
"""

import argparse
import sys
import os
from datetime import datetime
import logging

# Dodanie ścieżki src do PATH
sys.path.append('src')

from utils.config import config
from utils.helpers import create_experiment_folder, log_experiment


def setup_logging():
    """Konfiguruje logowanie"""
    logging.basicConfig(
        level=getattr(logging, config.get('logging.level', 'INFO')),
        format=config.get('logging.format', '%(asctime)s - %(levelname)s - %(message)s'),
        handlers=[
            logging.FileHandler(f"results/logs/main_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
            logging.StreamHandler()
        ]
    )


def run_data_exploration():
    """Uruchamia eksplorację danych"""
    logger = logging.getLogger(__name__)
    logger.info("Rozpoczynanie eksploracji danych...")
    
    # Import i uruchomienie eksploracji danych
    # from data.data_loader import load_retail_data, load_favorita_data
    # from utils.visualization import plot_time_series, plot_distribution
    
    logger.info("Eksploracja danych zakończona")


def run_preprocessing():
    """Uruchamia przetwarzanie danych"""
    logger = logging.getLogger(__name__)
    logger.info("Rozpoczynanie przetwarzania danych...")
    
    # Import i uruchomienie przetwarzania
    # from data.preprocessing import create_time_features, aggregate_daily_sales
    
    logger.info("Przetwarzanie danych zakończone")


def run_baseline_models():
    """Uruchamia modele bazowe"""
    logger = logging.getLogger(__name__)
    logger.info("Rozpoczynanie trenowania modeli bazowych...")
    
    # Import i uruchomienie modeli bazowych
    # from models.baseline_models import LinearRegressionModel, ProphetModel
    # from evaluation.metrics import calculate_metrics
    
    logger.info("Trenowanie modeli bazowych zakończone")


def run_neural_networks():
    """Uruchamia sieci neuronowe"""
    logger = logging.getLogger(__name__)
    logger.info("Rozpoczynanie trenowania sieci neuronowych...")
    
    # Import i uruchomienie sieci neuronowych
    # from models.neural_networks import MLPModel, LSTMModel
    # from evaluation.metrics import calculate_metrics
    
    logger.info("Trenowanie sieci neuronowych zakończone")


def run_model_comparison():
    """Uruchamia porównanie modeli"""
    logger = logging.getLogger(__name__)
    logger.info("Rozpoczynanie porównania modeli...")
    
    # Import i uruchomienie porównania
    # from evaluation.comparison import compare_models, plot_model_comparison
    
    logger.info("Porównanie modeli zakończone")


def main():
    """Główna funkcja"""
    parser = argparse.ArgumentParser(description='Projekt prognozowania popytu z sieciami neuronowymi')
    parser.add_argument('--experiment', type=str, required=True,
                       choices=['data_exploration', 'preprocessing', 'baseline', 
                               'neural_networks', 'comparison', 'all'],
                       help='Typ eksperymentu do uruchomienia')
    
    args = parser.parse_args()
    
    # Konfiguracja logowania
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info(f"Uruchamianie eksperymentu: {args.experiment}")
    logger.info(f"Konfiguracja załadowana z: {config.config_path}")
    
    # Tworzenie folderu dla eksperymentu
    experiment_folder = create_experiment_folder("results", args.experiment)
    logger.info(f"Folder eksperymentu: {experiment_folder}")
    
    try:
        if args.experiment == 'data_exploration' or args.experiment == 'all':
            run_data_exploration()
        
        if args.experiment == 'preprocessing' or args.experiment == 'all':
            run_preprocessing()
        
        if args.experiment == 'baseline' or args.experiment == 'all':
            run_baseline_models()
        
        if args.experiment == 'neural_networks' or args.experiment == 'all':
            run_neural_networks()
        
        if args.experiment == 'comparison' or args.experiment == 'all':
            run_model_comparison()
        
        logger.info("Eksperyment zakończony pomyślnie!")
        
    except Exception as e:
        logger.error(f"Błąd podczas wykonywania eksperymentu: {str(e)}")
        raise


if __name__ == "__main__":
    main()
