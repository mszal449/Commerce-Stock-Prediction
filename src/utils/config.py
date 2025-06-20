from pathlib import Path

# data preprocessing

DATA_DIR_DEFAULT = Path('/content/data')
OUT_DIR_DEFAULT  = Path('/content/data_processed')

LAG_LIST      = [7, 14, 28]
ROLL_WINDOWS  = [7, 28]
SEQ_LENGTH    = 60
PRED_LENGTH   = 15