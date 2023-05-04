import sys
sys.path.insert(0, '../')

import json
import requests
import pandas as pd
from datetime import datetime
from benzinga_tool import financial_data
from benzinga_tool import news_data
from benzinga_api.benzinga import * 

class ETL:
    def __init__(self, api_keys, start_day=None, end_day=None):
        self.api_keys = api_keys
        self.start_day = start_day
        self.end_day = end_day

class Benzinga(ETL):
    def __init__(self, ticker, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticker = ticker

    def get(self):
       news = news_data.News(self.api_keys['Benzinga'])
       df = benzinga_call(news, self.ticker, self.start_day, self.end_day)
       return df
    
    


