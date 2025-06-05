# Folder wyników

Ten folder zawiera wszystkie wyniki eksperymentów:

## Struktura:

- **models/**: Zapisane modele (.pkl, .h5, .joblib)
- **figures/**: Wykresy i wizualizacje (.png, .pdf)
- **metrics/**: Metryki i wyniki liczbowe (.json, .csv)
- **logs/**: Logi z eksperymentów (.log, .txt)

## Konwencja nazewnictwa:

### Modele:

- `baseline_linear_YYYY-MM-DD_HH-MM-SS.pkl`
- `baseline_prophet_YYYY-MM-DD_HH-MM-SS.pkl`
- `mlp_model_YYYY-MM-DD_HH-MM-SS.h5`
- `lstm_model_YYYY-MM-DD_HH-MM-SS.h5`

### Wykresy:

- `data_exploration_YYYY-MM-DD.png`
- `model_comparison_YYYY-MM-DD.png`
- `predictions_vs_actual_[model_name]_YYYY-MM-DD.png`
- `residuals_analysis_[model_name]_YYYY-MM-DD.png`

### Metryki:

- `experiment_results_YYYY-MM-DD.json`
- `model_comparison_YYYY-MM-DD.csv`
- `final_results.json`

### Logi:

- `experiment_YYYY-MM-DD.log`
- `training_log_[model_name]_YYYY-MM-DD.txt`
