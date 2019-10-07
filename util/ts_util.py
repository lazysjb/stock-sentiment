import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay


def shift_date_index(df,
                     n_days):
    """Shift by n business days"""
    shifted = df.copy()
    shifted.index = shifted.index + BDay(n=n_days)
    return shifted


def get_nday_pct_return(df, n_days):
    n_prev_df = shift_date_index(df, n_days)
    pct_return = (df - n_prev_df) / n_prev_df
    return pct_return


def calc_corr(df1,
              df2,
              df1_col,
              df2_col,
              method='pearson'):
    """df1 and df2 are assumed to have timeseries index"""
    merged = pd.merge(df1, df2, how='inner', left_index=True, right_index=True)
    corr_df = merged.corr(method=method)
    corr = corr_df[df1_col][df2_col]
    return corr


def reindex_weekend_to_monday(df,
                              agg_method='sum'):
    """Reindex weekend Twits to Monday since this happened after cob Friday"""
    new_df = df.copy()
    dt_idx = new_df.index
    next_biz_days = dt_idx + BDay(0)
    is_weekday_mask = dt_idx.map(lambda x: x.dayofweek < 5)
    new_df.index = np.where(is_weekday_mask, dt_idx, next_biz_days)

    if agg_method == 'sum':
        result = new_df.groupby(new_df.index).sum().sort_index()
    else:
        raise NotImplementedError('Not implemented for agg_method {}'.format(agg_method))

    return result


def resample_weekly(daily_df,
                    sample_freq='W-FRI',
                    agg_method='sum'):
    temp = daily_df.resample(sample_freq)

    if agg_method == 'sum':
        result = temp.sum()
    else:
        raise NotImplementedError('Not implemented for agg_method {}'.format(agg_method))

    return result


def rolling_nday(daily_df,
                 window='7D',
                 agg_method='sum'):
    # TODO(SJ): perhaps custom aggregation with using 5 business days
    #   may be more appropriate, but for now just using 7D window
    temp = daily_df.rolling(window)

    if agg_method == 'sum':
        result = temp.sum()
    else:
        raise NotImplementedError('Not implemented for agg_method {}'.format(agg_method))

    return result
