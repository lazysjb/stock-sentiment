import datetime
import warnings

import arrow
from arrow.factory import ArrowParseWarning

from config import STOCKTWITS_TICKER_LIST


# Disable Arrow warnings per https://github.com/crsmithdev/arrow/issues/612
warnings.simplefilter("ignore", ArrowParseWarning)


def get_all_stocktwits_tickers():
    return STOCKTWITS_TICKER_LIST


def get_est_market_datetime(orig_date_time):
    """If time is before market close, use the date otherwise use date + 1"""
    datetime_obj = arrow.get(orig_date_time, 'YYYY-MM-DD HH:mm:ss')

    # 4pm mkt close
    mkt_close_time = datetime.time(16, 0, 0)

    if datetime_obj.time() <= mkt_close_time:
        market_date = datetime_obj.strftime('%Y-%m-%d')
    else:
        market_date = datetime_obj.shift(days=1).strftime('%Y-%m-%d')
    return market_date


def append_market_date_col(stocktwit_raw_df,
                           mkt_date_col='mkt_date'):
    stocktwit_raw_df[mkt_date_col] = stocktwit_raw_df['created_at_est'].apply(
        get_est_market_datetime)


def get_daily_sentiment_count_df(stocktwit_raw_df,
                                 mkt_date_col='mkt_date',
                                 sentiment_col='entities.sentiment.basic'):
    append_market_date_col(stocktwit_raw_df, mkt_date_col=mkt_date_col)

    grouped = stocktwit_raw_df.groupby(
        mkt_date_col)[sentiment_col].value_counts().to_frame('count').reset_index()
    daily_sentiment_count_df = grouped.pivot(index=mkt_date_col,
                                             columns=sentiment_col,
                                             values='count').fillna(0)
    daily_sentiment_count_df.columns.name = None
    daily_sentiment_count_df = daily_sentiment_count_df.sort_index()

    return daily_sentiment_count_df
