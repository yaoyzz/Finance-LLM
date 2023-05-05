import json
import pandas as pd
from api_etl.etl import *
from api_etl.benzinga import *
from api_etl.yahoofinance import *
from api_etl.fred import *
from api_etl.youtube import *


if __name__ == "__main__":
    with open("api-keys.json", "r") as f:
        api_keys = json.load(f)
        print(api_keys)

    fromdate = "2019-01-01"
    todate = "2023-05-03"
    
    #------------------------------uncomment to fetch data-------------------------------
    #------------------------------pull Benziga news data--------------------------------
    # tick_list = ['MSFT', 'JNJ', 'INTC', 'BA', 'UNH', 
    #         'JPM', 'V', 'PG', 'HD', 'CVX', 
    #         'MRK', 'KO', 'CSCO', 'MCD','WMT', 
    #         'CRM', 'DIS', 'VZ', 'NKE', 'AAPL', 
    #         'IBM', 'GS', 'HON', 'AXP', 'AMGN']
    
    # Benzinga.pull_batch_benzinga(api_keys, tick_list, fromdate, todate)
    
    #------------------------------pull yahoo stock data---------------------------------
    # tick_list = ['SPY']

    # yahoo = Yahoo(tick_list, api_keys, fromdate, todate)
    # yahoo.fetch_data()
    # yahoo.add_technical_indicators()
    # yahoo.add_vix()
    # yahoo.add_bond()
    # yahoo.export_as_csv()

    #----------------------------pull macro economics data-------------------------------
    # fred = Fredapi(api_keys, fromdate, todate)
    # fred.fetch_macro_data()
    
    #----------------------------pull youtube data-------------------------------
    # tube = Youtube(api_keys = api_keys, channel_name = 'The Stocks Channel', start_day = fromdate, endday = todate)
    # tube.get()
    






