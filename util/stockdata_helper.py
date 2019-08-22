from config import STOCKDATA_TICKER_LIST
from util.file_util import StockDataFileReader


def get_stockdata_tickers():
    return STOCKDATA_TICKER_LIST


def get_daily_returns_for_ticker(ticker,
                                 start_date,
                                 end_date,
                                 columns=['adjusted close'],
                                 return_type='pct'):
    stock_data_reader = StockDataFileReader()
    ts_df = stock_data_reader.read_stockdata_in_range(ticker,
                                                      start_date,
                                                      end_date,
                                                      columns=['date'] + columns)
    if return_type == 'pct':
        return_df = ts_df.pct_change()
    else:
        raise NotImplementedError('return type {} not implemented'.format(return_type))

    col_name_map = {}
    for c in columns:
        col_name_map[c] = c + ' return'
    return_df = return_df.rename(columns=col_name_map)

    return return_df


def get_mkt_adjusted_returns_for_ticker(ticker,
                                        start_date,
                                        end_date,
                                        return_type='pct'):
    """Define mkt adjusted as ticker return - SPX return"""
    ticker_return_df = get_daily_returns_for_ticker(ticker, start_date, end_date,
                                                    return_type=return_type)
    mkt_return_df = get_daily_returns_for_ticker(ticker, start_date, end_date,
                                                 return_type=return_type)
    mkt_adjusted_return = ticker_return_df - mkt_return_df
    return mkt_adjusted_return
