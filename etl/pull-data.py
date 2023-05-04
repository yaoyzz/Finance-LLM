import json
import requests
import pandas as pd
from datetime import datetime
from benzinga_tool import financial_data
from benzinga_tool import news_data
from benzinga_api.benzinga import * 
from etl.etl import *
from etl.etl import Benzinga

def pull_benzinga_news(tick_list, start_day, end_day):
    df_list = []
    for ticker in tick_list:
        news = Benzinga(api_keys = api_keys, ticker = ticker, start_day = start_day, end_day = end_day)
        df_list.append( news.get() )
    df = pd.concat(df_list, axis=0)
    df = df.sort_values(by='created')
    df.to_csv('benzinga.csv', index=False)

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
    
    pull_benzinga_news(tick_list, fromdate, todate)
    




