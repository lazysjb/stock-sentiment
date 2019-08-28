STOCKTWITS_ROOT_DIR = '/Users/seung-jae_bang/Personal/Research/Stock_Sentiment/data/Stocktwits'
STOCKDATA_ROOT_DIR = '/Users/seung-jae_bang/Personal/Research/Stock_Sentiment/data/AlphaVantage'

STOCKTWITS_TICKER_LIST = [
    # Intial List
    'SHAK',     # Shakeshack
    'MSFT',     # Microsoft
    'TSLA',     # Tesla
    'SBUX',     # Starbucks

    # 2019 IPO Stocks
    'BYND',  # Beyond Meat
    'UBER',  # Uber
    'LYFT',  # Lyft
    'WORK',  # Slack
    'ZM',  # Zoom
    'PINS',  # Pinterest
    'CHWY',  # Chewy
    'CRWD',  # Crowdstrike

    # MID CAP STOCK SELECTION #

    # Top 10 Holdings
    'IEX',
    'STE',
    'LDOS',
    'ZBRA',
    'NVR',
    'ODFL',
    'TRMB',
    'FDS',
    'TDY',
    'WST',

    # Random select 20
    'PTC',
    'AEO',
    'HOMB',
    'OSK',
    'SXT',
    'BOH',
    'GME',
    'AFG',
    'EAT',
    'NUVA',
    'AVNS',
    'CNO',
    'CDK',
    'SON',
    'JACK',
    'GHC',
    'WWE',
    'TFX',
    'SIG',
    'PLT',
]
STOCKDATA_TICKER_LIST = STOCKTWITS_TICKER_LIST + [
    # SP500 ETF
    'SPY',
]

IPO_START_DATE_MAP = {
    'BYND': '2019-05-03',
    'UBER': '2019-05-10',
    'LYFT': '2019-03-29',
    'WORK': '2019-06-21',
    'ZM': '2019-04-18',
    'PINS': '2019-04-18',
    'CHWY': '2019-06-14',
    'CRWD': '2019-06-14',
}
