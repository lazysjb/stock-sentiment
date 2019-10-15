import funcy
import pandas as pd

from config import (
    ETF_TICKER_TO_SECTOR, GICS_SECTOR_LIST, SP_500_COMPONENT_SECTOR_MAP_FILE,
    STOCKDATA_TICKER_LIST, STOCKTWITS_BAD_TICKER_LIST)
from util.file_util import StockDataFileReader
from util.ts_util import get_nday_pct_return


def get_stockdata_tickers():
    return STOCKDATA_TICKER_LIST


def get_sector_etf_ticker_map():
    return ETF_TICKER_TO_SECTOR


def get_etf_ticker_for_sector(sector):
    etf_ticker = funcy.flip(get_sector_etf_ticker_map())[sector]
    return etf_ticker


def get_component_tickers_for_sector(sector,
                                     exclude_bad_stocktwit_tickers=True):
    sp500_sector_info = get_sp500_sector_info(exclude_bad_stocktwit_tickers)

    if sector == 'All':
        ticker_list = sp500_sector_info['ticker'].tolist()
    else:
        ticker_list = sp500_sector_info.loc[
            sp500_sector_info['GICS_Sector'] == sector, 'ticker'].tolist()
    return ticker_list


def get_sp500_sector_info(exclude_bad_stocktwit_tickers=True):
    df = pd.read_csv(SP_500_COMPONENT_SECTOR_MAP_FILE)

    if exclude_bad_stocktwit_tickers:
        df = df[~df['ticker'].isin(STOCKTWITS_BAD_TICKER_LIST)].copy()
    return df


def get_gics_sector_list(exclude_comms=True):
    """Since communication sector etf was created 2018-07, skip this"""
    if exclude_comms:
        sector_list = [s for s in GICS_SECTOR_LIST if s != 'Communication Services']
    else:
        sector_list = GICS_SECTOR_LIST

    return sector_list


def get_nday_returns_for_ticker(ticker,
                                start_date,
                                end_date,
                                n_days=1,
                                columns=['adjusted close'],
                                return_type='pct'):
    stock_data_reader = StockDataFileReader()
    ts_df = stock_data_reader.read_stockdata_in_range(ticker,
                                                      start_date,
                                                      end_date,
                                                      columns=['date'] + columns)
    if return_type == 'pct':
        if n_days == 1:
            return_df = ts_df.pct_change()
        else:
            return_df = get_nday_pct_return(ts_df, n_days)
    else:
        raise NotImplementedError('return type {} not implemented'.format(return_type))

    col_name_map = {}
    for c in columns:
        col_name_map[c] = c + ' return'
    return_df = return_df.rename(columns=col_name_map)

    return return_df


def get_nday_mkt_adjusted_returns_for_ticker(ticker,
                                             start_date,
                                             end_date,
                                             n_days=1,
                                             return_type='pct',
                                             mkt_ticker='SPY'):
    """Define mkt adjusted as ticker return - SPY return"""
    ticker_return_df = get_nday_returns_for_ticker(ticker, start_date, end_date,
                                                   n_days=n_days, return_type=return_type)
    mkt_return_df = get_nday_returns_for_ticker(mkt_ticker, start_date, end_date,
                                                n_days=n_days, return_type=return_type)
    mkt_adjusted_return = ticker_return_df - mkt_return_df
    return mkt_adjusted_return
