from datetime import datetime
from glob import glob
import os

import pandas as pd

from config import STOCKDATA_ROOT_DIR, STOCKTWITS_ROOT_DIR


_STOCK_TWIT_FILE_FORMAT = '{ticker}_{date_str}.json'
_STOCK_TWIT_FILE_FORMAT_ALL = '{ticker}_*.json'

_STOCK_TWIT_DEFAULT_COLS = [
    'date_est',
    'created_at_est',
    'body',
    'symbols',
    'entities.sentiment.basic',
    'links',
]

_STOCK_DATA_FILE_FORMAT = '{ticker}.json'


class StockTwitsFileReader:

    def __init__(self, root_dir=STOCKTWITS_ROOT_DIR):
        self.root_dir = root_dir

    def get_root_dir(self):
        return self.root_dir

    def get_subdir_for_ticker(self, ticker):
        return os.path.join(self.root_dir, 'raw', ticker)

    def get_all_files_for_ticker(self, ticker):
        subdir = self.get_subdir_for_ticker(ticker)
        file_paths = glob(os.path.join(subdir,
                                       _STOCK_TWIT_FILE_FORMAT_ALL.format(ticker=ticker)))
        return file_paths

    def _validate_date_format(self, date):
        """Validate that date is in format YYYY-MM-DD"""
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError('date {} is in incorrect format'.format(date))

    def get_twit_file_path(self, ticker, date):
        self._validate_date_format(date)

        return os.path.join(self.get_subdir_for_ticker(ticker),
                            _STOCK_TWIT_FILE_FORMAT.format(ticker=ticker, date_str=date))

    def get_twit_file_paths_in_range(self, ticker, start_date, end_date):
        self._validate_date_format(start_date)
        self._validate_date_format(end_date)

        candidate_file_paths = self.get_all_files_for_ticker(ticker)
        candidate_file_paths = [(f, f.split('_')[-1].split('.')[0]) for f in candidate_file_paths]
        file_paths = [x for x in candidate_file_paths if start_date <= x[1] <= end_date]
        file_paths = sorted(file_paths, key=lambda x: x[1])
        file_paths = [f[0] for f in file_paths]
        return file_paths

    def read_json_file_to_df(self, file_path):
        return pd.read_json(file_path, orient='records', lines=True)

    def read_twit_file(self, ticker, date, cols='all'):
        file_path = self.get_twit_file_path(ticker, date)
        df = self.read_json_file_to_df(file_path)

        if cols == 'default':
            df = df[_STOCK_TWIT_DEFAULT_COLS].copy()
        elif cols != 'all':
            df = df[cols].copy()
        return df

    def read_twit_file_in_range(self, ticker, start_date, end_date, cols='all'):
        file_paths = self.get_twit_file_paths_in_range(ticker, start_date, end_date)

        dfs = []
        for fp in file_paths:
            dfs.append(self.read_json_file_to_df(fp))

        result_df = pd.concat(dfs, sort=True).reset_index(drop=True)

        if cols == 'default':
            result_df = result_df[_STOCK_TWIT_DEFAULT_COLS].copy()
        elif cols != 'all':
            result_df = result_df[cols].copy()
        return result_df


class StockDataFileReader:

    def __init__(self, root_dir=STOCKDATA_ROOT_DIR):
        self.root_dir = root_dir

    def get_subdir(self, data_type='stock_data'):
        if data_type == 'stock_data':
            subdir = os.path.join(self.root_dir, 'stock_data')
        elif data_type == 'meta':
            subdir = os.path.join(self.root_dir, 'meta')
        else:
            raise ValueError('Incorrect data_type arg value of {}'.format(data_type))

        return subdir

    def get_stockdata_file_path(self, ticker, data_type='stock_data'):
        file_path = os.path.join(self.get_subdir(data_type=data_type),
                                 _STOCK_DATA_FILE_FORMAT.format(ticker=ticker))
        return file_path

    def read_stockdata_from_json(self, ticker):
        file_path = self.get_stockdata_file_path(ticker, data_type='stock_data')
        df = pd.read_json(file_path, orient='records', lines=True)

        return df

    def read_stockdata_in_range(self,
                                ticker,
                                start_date,
                                end_date,
                                columns=['date', 'adjusted close'],
                                date_as_index=True):
        df = self.read_stockdata_from_json(ticker)

        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        df = df[columns].copy()

        if date_as_index:
            df = df.set_index('date').sort_index()

        return df
