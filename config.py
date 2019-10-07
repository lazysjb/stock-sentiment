import pandas as pd


STOCKTWITS_ROOT_DIR = '/Users/seung-jae_bang/Personal/Research/Stock_Sentiment/data/Stocktwits'
STOCKDATA_ROOT_DIR = '/Users/seung-jae_bang/Personal/Research/Stock_Sentiment/data/AlphaVantage'


SP_500_COMPONENT_TICKER_FILE = ('/Users/seung-jae_bang/Personal/Research/'
                                'Stock_Sentiment/ingest_code/data-ingest/'
                                'data/sp_500_component.csv')
SP_500_COMPONENT_SECTOR_MAP_FILE = ('/Users/seung-jae_bang/Personal/Research/'
                                    'Stock_Sentiment/ingest_code/data-ingest/'
                                    'data/sp_500_component_sector_map_wiki.csv')

# For some reason I can't query the below tickers in StockTwits
STOCKTWITS_BAD_TICKER_LIST = [
    'GL', 'AMCR', 'FOX',
]


def _get_sp_500_ticker_list_from_file():
    df = pd.read_csv(SP_500_COMPONENT_TICKER_FILE)
    ticker_list = df['ticker'].tolist()
    ticker_list = list(set(ticker_list) - set(STOCKTWITS_BAD_TICKER_LIST))
    return ticker_list


STOCKTWITS_TICKER_LIST = _get_sp_500_ticker_list_from_file() + [
    # # Intial List
    # 'SHAK',     # Shakeshack
    # 'MSFT',     # Microsoft
    # 'TSLA',     # Tesla
    # 'SBUX',     # Starbucks
    #
    # # 2019 IPO Stocks
    # 'BYND',  # Beyond Meat
    # 'UBER',  # Uber
    # 'LYFT',  # Lyft
    # 'WORK',  # Slack
    # 'ZM',  # Zoom
    # 'PINS',  # Pinterest
    # 'CHWY',  # Chewy
    # 'CRWD',  # Crowdstrike
    #
    # # MID CAP STOCK SELECTION #
    #
    # # Top 10 Holdings
    # 'IEX',
    # 'STE',
    # 'LDOS',
    # 'ZBRA',
    # 'NVR',
    # 'ODFL',
    # 'TRMB',
    # 'FDS',
    # 'TDY',
    # 'WST',
    #
    # # Random select 20
    # 'PTC',
    # 'AEO',
    # 'HOMB',
    # 'OSK',
    # 'SXT',
    # 'BOH',
    # 'GME',
    # 'AFG',
    # 'EAT',
    # 'NUVA',
    # 'AVNS',
    # 'CNO',
    # 'CDK',
    # 'SON',
    # 'JACK',
    # 'GHC',
    # 'WWE',
    # 'TFX',
    # 'SIG',
    # 'PLT',
]

ETF_TICKER_TO_SECTOR = {
    'XLF': 'Financials',
    'XLU': 'Utilities',
    'XLP': 'Consumer Staples',
    'XLK': 'Information Technology',
    'XLI': 'Industrials',
    'XLB': 'Materials',
    'XLC': 'Communication Services',
    'XLV': 'Health Care',
    'XLY': 'Consumer Discretionary',
    'XLRE': 'Real Estate',
    'XLE': 'Energy',

    'SPY': 'All',
}

GICS_SECTOR_LIST = [
    'Consumer Staples',
    'Real Estate',
    'Industrials',
    'Information Technology',
    'Communication Services',
    'Energy',
    'Materials',
    'Consumer Discretionary',
    'Financials',
    'Health Care',
    'Utilities',

    'All',  # Not really a sector but just my notation of include all sp500
]

SECTOR_ETF_TICKERS = [
    # Sector ETFs
    # https://etfdb.com/compare/volume/
    'XLF',      # Financial sector
    'XLU',      # Utilities sector
    'XLP',      # Consumer Staples sector
    'XLK',      # Technology sector
    'XLI',      # Industrial sector
    'XLB',      # Materials sector
    'XLC',      # Communication Services sector
    'XLV',      # Health Care sector
    'XLY',      # Consumer Discretionary sector
    'XLRE',     # Real Estate sector
    'XLE',      # Energy sector

]

STOCKDATA_TICKER_LIST = STOCKTWITS_TICKER_LIST + [
    # SP500 ETF
    'SPY',
] + SECTOR_ETF_TICKERS

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
