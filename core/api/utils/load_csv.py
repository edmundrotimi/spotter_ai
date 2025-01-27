import os

import pandas as pd

from core.project.settings import BASE_DIR


def pandas_load_csv():
    # load and read csv file
    file_path = os.path.join(BASE_DIR, 'core/fuel/utils/fuel-prices-for-be-assessment.csv')
    df = pd.read_csv(file_path)

    return df


def pandas_load_update_csv():
    # load and read csv file
    file_path = os.path.join(BASE_DIR, 'core/fuel/utils/update_fuel-prices-for-be-assessment.csv')
    df = pd.read_csv(file_path)

    return df
