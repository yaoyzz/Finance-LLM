import json
import requests
import pandas as pd
from datetime import datetime
from benzinga_tool import financial_data
from benzinga_tool import news_data
from benzinga_api.benzinga_api import * 
from etl.etl import *
from etl.benzinga import *

if __name__ == "__main__":
    with open("api-keys.json", "r") as f:
        api_keys = json.load(f)
        print(api_keys)

    fromdate = "2019-01-01"
    todate = "2023-05-03"
    
    #------------------------------pull Benziga news data--------------------------------
    tick_list = ['MSFT', 'JNJ', 'INTC', 'BA', 'UNH', 
            'JPM', 'V', 'PG', 'HD', 'CVX', 
            'MRK', 'KO', 'CSCO', 'MCD','WMT', 
            'CRM', 'DIS', 'VZ', 'NKE', 'AAPL', 
            'IBM', 'GS', 'HON', 'AXP', 'AMGN']
    
    Benzinga.pull_benzinga_news(api_keys, tick_list, fromdate, todate)
    




