from pathlib import Path

PROJECT_PATH = Path(__file__).parent
DATA_PATH = PROJECT_PATH / 'data'
DATABASE_PATH = f'{DATA_PATH.absolute().as_posix()}/data_for_training_db.sqlite'
TRAINING_REPORT_PATH = DATA_PATH / 'model_training_report'

BOT_TOKEN = '7825368344:AAHrruIowdwIr0m_mwQi-OM0M_mZxtEXl-U'
SUPPORTED_DATASET_TYPES = ['csv']
AVAILABLE_TASK_TYPES = ['reg', 'binary', 'multiclass', 'multi:reg', 'multilabel']
AVAILABLE_MODELS = ['lgb', 'lgb_tuned', 'linear_l2', 'cb', 'cb_tuned', 'auto', 'xgb', 'xgb_tuned'] # проверить, все ли поддерживаются

RANDOM_STATE = 42
N_FOLDS = 3