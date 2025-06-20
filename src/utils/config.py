from pathlib import Path

# data preprocessing

PROJECT_ROOT      = Path(__file__).resolve().parents[2]  
DATA_DIR_DEFAULT  = PROJECT_ROOT / 'data' / 'raw'
OUT_DIR_DEFAULT   = PROJECT_ROOT / 'data' / 'processed'

LAG_LIST      = [7, 14, 28]
ROLL_WINDOWS  = [7, 28]
SEQ_LENGTH    = 60
PRED_LENGTH   = 15