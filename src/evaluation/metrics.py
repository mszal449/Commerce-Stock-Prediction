"""evaluation_metrics.py
Utility functions for scoring demand-forecast models

Available metrics
-----------------
* mae - Mean Absolute Error
* rmse - Root Mean Squared Error
* rmsle - Root Mean Squared Log Error (Kaggle leaderboard target)
* mape -Mean Absolute Percentage Error
* smape - Symmetric MAPE (robust to low denominators)
* nwrmsle - Normalised, Weighted RMSLE (optional daily weights)
* summary - Convenience wrapper that returns a dict of all metrics
"""

from __future__ import annotations

import time
from typing import Dict, Any, Sequence

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(mean_absolute_error(y_true, y_pred))

def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))

def rmsle(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-6) -> float:
    return float(np.sqrt(mean_squared_log_error(y_true, np.maximum(0, y_pred) + eps)))

def mape(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-6) -> float:
    return float(np.mean(np.abs((y_true - y_pred) / np.clip(y_true, eps, None))))

def smape(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-6) -> float:
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2.0
    return float(np.mean(np.abs(y_true - y_pred) / np.clip(denom, eps, None)))

def nwrmsle(y_true: np.ndarray, y_pred: np.ndarray, weights: Sequence[float] | None = None,
            eps: float = 1e-6) -> float:
    if weights is None:
        return rmsle(y_true, y_pred, eps)

    w = np.asarray(weights, dtype=float)
    log_diff = np.log1p(np.maximum(0, y_pred) + eps) - np.log1p(y_true + eps)
    return float(np.sqrt(np.sum(w * log_diff ** 2) / np.sum(w)))

def summary(y_true: np.ndarray, y_pred: np.ndarray,
            extra: Dict[str, Any] | None = None) -> Dict[str, float]:
    res: Dict[str, float] = {
        'MAE':   mae(y_true, y_pred),
        'RMSE':  rmse(y_true, y_pred),
        'RMSLE': rmsle(y_true, y_pred),
        'MAPE':  mape(y_true, y_pred),
        'SMAPE': smape(y_true, y_pred),
    }
    if extra:
        res.update(extra)
    return res

def timed(func):
    def _timed(*args, **kwargs):
        t0 = time.time()
        out = func(*args, **kwargs)
        return out, time.time() - t0
    return _timed
