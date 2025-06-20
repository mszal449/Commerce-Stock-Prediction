"""
Moduł do przetwarzania i transformacji danych dla konkursu Kaggle
**Store Sales - Time Series Forecasting**.

Funkcja **`preprocess_data`** wykonuje kompletny pipeline:

1. Wczytanie sześciu plików CSV (train / test / stores / oil / holidays / transactions)
2. Czyszczenie duplikatów i przycięcie outlierów (górny 0.1 %) w `sales`
3. Inżynieria cech kalendarzowych i kategorycznych
4. Scalanie tabel zewnętrznych (WTI, święta, transakcje, meta-sklepów)
5. Lagi oraz statystyki kroczące dla `(store_nbr, family)`
6. Standaryzacja kolumn zmiennoprzecinkowych i zapis skalerów
7. Chronologiczny split -> train / validation / test (domyślnie 15-dniowy horyzont)
8. (Opcjonalnie) budowa 60-dniowych sekwencji LSTM oraz zapis *.npz*

"""

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

from src.utils.config import DATA_DIR_DEFAULT, OUT_DIR_DEFAULT, LAG_LIST, SEQ_LENGTH, PRED_LENGTH, ROLL_WINDOWS

def load_raw(path: Path) -> Dict[str, pd.DataFrame]:
    files = {f.stem: f for f in path.glob('*.csv')}
    required = ["train", "test", "stores", "oil", "holidays_events", "transactions"]
    missing  = [k for k in required if k not in files]
    if missing:
        raise FileNotFoundError(f"Missing files: {missing}")

    return {
        'train':  pd.read_csv(files['train'],  parse_dates=['date']),
        'test':   pd.read_csv(files['test'],   parse_dates=['date']),
        'stores': pd.read_csv(files['stores']),
        'oil':    pd.read_csv(files['oil'],    parse_dates=['date']),
        'holidays':     pd.read_csv(files['holidays_events'], parse_dates=['date']),
        'transactions': pd.read_csv(files['transactions'],   parse_dates=['date']),
    }

def basic_clean(train: pd.DataFrame) -> pd.DataFrame:
    before = len(train)
    train = train.drop_duplicates(subset=['date', 'store_nbr', 'family'])
    print(f"Dropped {before - len(train):,} duplicate rows")

    upper = train['sales'].quantile(0.999)
    train['sales'] = train['sales'].clip(upper=upper)
    return train

def add_calendar(df: pd.DataFrame) -> pd.DataFrame:
    d = df['date']
    df['year']      = d.dt.year.astype('int16')
    df['month']     = d.dt.month.astype('int8')
    df['dow']       = d.dt.weekday.astype('int8')
    df['weekofyr']  = d.dt.isocalendar().week.astype('int8')

    df['dow_sin']   = np.sin(2 * np.pi * df['dow']   / 7)
    df['dow_cos']   = np.cos(2 * np.pi * df['dow']   / 7)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    return df

def merge_external(train: pd.DataFrame, raw: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    oil = raw['oil'].set_index('date').reindex(
        pd.date_range('2013-01-01', '2017-08-31', freq='D'))
    oil['dcoilwtico'] = oil['dcoilwtico'].interpolate().ffill().bfill()
    oil['oil_ma30']   = oil['dcoilwtico'].rolling(30).mean()
    oil['oil_pct_7']  = oil['dcoilwtico'].pct_change(7)
    oil = oil.reset_index().rename(columns={'index': 'date'})

    hol = raw['holidays']
    nat_hol = hol[(hol['locale'] == 'National') & (~hol['transferred'])]
    nat_flag = pd.DataFrame({'date': nat_hol['date'].dt.normalize(), 'is_natl_holiday': 1})

    tx = (raw['transactions']
          .groupby('date')['transactions']
          .sum()
          .rolling(7).mean()
          .reset_index())

    df = (train
          .merge(oil, on='date', how='left')
          .merge(nat_flag, on='date', how='left')
          .merge(tx, on='date', how='left')
          .merge(raw['stores'], on='store_nbr', how='left'))

    df['is_natl_holiday'] = df['is_natl_holiday'].fillna(0).astype('int8')
    df['transactions']    = df['transactions'].fillna(method='ffill').fillna(0)
    return df

def add_lags(df: pd.DataFrame, group_cols: List[str]) -> pd.DataFrame:
    g = df.sort_values('date').groupby(group_cols)
    for lag in LAG_LIST:
        df[f'lag_{lag}'] = g['sales'].shift(lag)
    for win in ROLL_WINDOWS:
        df[f'roll_mean_{win}'] = g['sales'].shift(1).rolling(win).mean()
        df[f'roll_std_{win}']  = g['sales'].shift(1).rolling(win).std()
    df['is_zero'] = (df['sales'] == 0).astype('int8')
    return df

def scale_numeric(df: pd.DataFrame, out_dir: Path) -> Dict[str, StandardScaler]:
    num_cols = df.select_dtypes(include=['float64', 'float32']).columns.tolist()
    scalers = {}
    for col in num_cols:
        sc = StandardScaler()
        df[col] = sc.fit_transform(df[[col]])
        scalers[col] = sc
    joblib.dump(scalers, out_dir / 'scalers.pkl')
    return scalers

def chrono_split(df: pd.DataFrame,
                 train_end: str = '2016-12-31',
                 val_end: str   = '2017-06-30') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train = df[df['date'] <= train_end]
    val   = df[(df['date'] > train_end) & (df['date'] <= val_end)]
    test  = df[df['date'] > val_end]
    return train, val, test

def build_sequences(df: pd.DataFrame, group_cols: List[str]) -> Tuple[np.ndarray, np.ndarray]:
    X_list, y_list = [], []
    feature_cols = df.columns.difference(['sales', 'date']).tolist()

    for _, grp in df.groupby(group_cols):
        grp = grp.sort_values('date')
        Xv = grp[feature_cols].values.astype(np.float32)
        yv = grp['sales'].values.astype(np.float32)
        for i in range(SEQ_LENGTH, len(grp) - PRED_LENGTH + 1):
            X_list.append(Xv[i - SEQ_LENGTH:i])
            y_list.append(yv[i:i + PRED_LENGTH])

    return np.stack(X_list), np.stack(y_list)

def preprocess_data(data_dir: Path | str = DATA_DIR_DEFAULT,
                    out_dir: Path | str  = OUT_DIR_DEFAULT,
                    build_seq: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run the full preprocessing pipeline and return train/val/test DataFrames.

    build_seq : bool, default False
        If True, additionally create LSTM tensors (60-day history, 15-day horizon)
        and save them as 'lstm_data.npz'.
    """
    data_dir = Path(data_dir)
    out_dir  = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = load_raw(data_dir)

    train = basic_clean(raw['train'])
    train = add_calendar(train)
    train = merge_external(train, raw)
    train = add_lags(train, ['store_nbr', 'family'])

    train.dropna(inplace=True)

    scale_numeric(train, out_dir)

    train_df, val_df, test_df = chrono_split(train)

    train_df.to_parquet(out_dir / 'train.parquet')
    val_df.to_parquet(out_dir / 'val.parquet')
    test_df.to_parquet(out_dir / 'test.parquet')

    if build_seq:
        Xtr, ytr = build_sequences(train_df, ['store_nbr', 'family'])
        Xval, yval = build_sequences(val_df, ['store_nbr', 'family'])
        Xte, yte   = build_sequences(test_df, ['store_nbr', 'family'])
        np.savez_compressed(out_dir / 'lstm_data.npz',
                            X_train=Xtr, y_train=ytr,
                            X_val=Xval,  y_val=yval,
                            X_test=Xte,  y_test=yte)

    return train_df, val_df, test_df
