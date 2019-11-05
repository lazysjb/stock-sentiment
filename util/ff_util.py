"""Util to process Fama French factors"""
import os

import pandas as pd

FF_DAILY_RETURNS_FILEPATH = os.path.join(os.path.dirname(__file__),
                                         '../data/F-F_Research_Data_Factors_daily.CSV')
FF_DAILY_MOMENTUM_FILEPATH = os.path.join(os.path.dirname(__file__),
                                          '../data/F-F_Momentum_Factor_daily.CSV')


def read_ff_factors_daily(filepath=FF_DAILY_RETURNS_FILEPATH,
                          include_momentum=True):
    ff_df = pd.read_csv(filepath,
                        skiprows=[0, 1, 2])
    ff_df_cols = ff_df.columns.values
    ff_df_cols[0] = 'date'
    ff_df.columns = ff_df_cols

    ff_df = ff_df.drop('RF', axis=1)
    # last row has copyright info
    ff_df = ff_df.iloc[:-1].copy()
    ff_df['date'] = pd.to_datetime(ff_df['date'])

    ff_df = ff_df.set_index('date').sort_index().copy()
    # Original unit is in %, converting to raw units
    ff_df = ff_df / 100

    if include_momentum:
        mom_df = read_momentum_factor_daily()
        ff_df = ff_df.merge(mom_df, left_index=True, right_index=True)

    return ff_df


def read_momentum_factor_daily(filepath=FF_DAILY_MOMENTUM_FILEPATH):
    mom_df = pd.read_csv(filepath,
                         skiprows=14,
                         header=None,
                         names=['date', 'Mom'])
    # last row has copyright info
    mom_df = mom_df.iloc[:-1].copy()
    mom_df['date'] = pd.to_datetime(mom_df['date'])

    mom_df = mom_df.set_index('date').sort_index().copy()
    # Original unit is in %, converting to raw units
    mom_df = mom_df / 100
    return mom_df


def get_ff_factors_with_freq(filepath=FF_DAILY_RETURNS_FILEPATH,
                             freq='W-FRI'):
    ff_df_daily = read_ff_factors_daily(filepath=filepath)
    ff_df_temp = ff_df_daily + 1
    result = ff_df_temp.resample(freq).apply(lambda g: g.prod(axis=0)) - 1
    return result
