import matplotlib.pyplot as plt
import matplotlib.dates as md

from util.file_util import StockDataFileReader, StockTwitsFileReader
from util.ts_util import resample_weekly


def plot_time_series(df,
                     figsize=(8, 6),
                     title=None):
    """Assume input dataframe (df) has index as dates"""
    fig, ax = plt.subplots(figsize=figsize)
    df.plot(ax=ax)

    if title is not None:
        ax.set_title(title)


def _xaxis_custom_date_format(ax):
    myFmt = md.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_locator(
        #     matplotlib.dates.WeekdayLocator(byweekday=matplotlib.dates.MO)
        md.MonthLocator()
    )
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis.set_tick_params(rotation=45)


def plot_time_series_bar(df,
                         figsize=(8, 6),
                         title=None):
    """The date legend gets ugly by default"""
    fig, ax = plt.subplots(figsize=figsize)

    bar_setting = [
        {'offset': 0, 'color': 'orange', 'width': 2},
        {'offset': -2, 'color': 'g', 'width': 2},
    ]
    bar_plots = []
    num_dates = md.date2num(df.index)

    for i, col in enumerate(df.columns):
        temp = ax.bar(num_dates + bar_setting[i]['offset'],
                      df[col],
                      label=col,
                      color=bar_setting[i]['color'], width=bar_setting[i]['width'], align='center')
        bar_plots.append(temp)

    _xaxis_custom_date_format(ax)

    ax.legend('upper right', handles=bar_plots)

    if title is not None:
        ax.set_title(title)
    return ax


def overlay_on_secondary_axis(df, col_name, primary_ax):
    secondary_ax = primary_ax.twinx()
    _ = secondary_ax.plot(df.index, df[col_name], linewidth=0.7, linestyle='--')
    return


def plot_twit_series_for_ticker(ticker,
                                start_date,
                                end_date,
                                overlay_price=True,
                                freq='w'):
    twit_file_reader = StockTwitsFileReader()
    twit_df = twit_file_reader.read_daily_sentiment_summary_prelim(ticker,
                                                                   start_date=start_date,
                                                                   end_date=end_date)
    if freq == 'w':
        twit_df = resample_weekly(twit_df)
    else:
        raise ValueError('Unrecognized freq {}'.format(freq))

    ax = plot_time_series_bar(twit_df,
                              figsize=(14, 5), )

    if overlay_price:
        stock_file_reader = StockDataFileReader()
        price_df = stock_file_reader.read_stockdata_in_range(ticker,
                                                             start_date,
                                                             end_date)
        overlay_on_secondary_axis(price_df, 'adjusted close', ax)

    return
