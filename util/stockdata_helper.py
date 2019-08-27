from config import STOCKDATA_TICKER_LIST
from util.file_util import StockDataFileReader
from util.ts_util import get_nday_pct_return


def get_stockdata_tickers():
    return STOCKDATA_TICKER_LIST


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
