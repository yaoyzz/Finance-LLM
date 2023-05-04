import sys
sys.path.insert(0, '../')

from benzinga import financial_data
from benzinga import news_data
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import json
import inspect
import datetime

api_key = "318da1f2bee64e3caf1c22dfb78f70d1"
news = news_data.News(api_key)

def process_stories(stories):
    df = pd.DataFrame(stories)[['created', 'title', 'body']]
    df['created'] = pd.to_datetime(df['created'], errors='coerce')
    # Remove HTML tags using Beautiful Soup
    df['body'] = df['body'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())
    df = df.dropna(subset=['created', 'title', 'body'])
    df['created'] = df['created'].dt.date
    return df

def benzinga_call(ticker, fromdate, todate):
    stories = news.news(display_output='full', company_tickers=ticker, pagesize=100, date_from=fromdate, date_to=todate)
    df = process_stories(stories)

    fromdate = (df.iloc[-1, 0] - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    one_month_be4_todate = (datetime.datetime.strptime(todate, '%Y-%m-%d') - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    last_request_fromdate = None
    while fromdate < one_month_be4_todate:
        if last_request_fromdate is not None and fromdate <= last_request_fromdate:
            fromdate = (datetime.datetime.strptime(last_request_fromdate, '%Y-%m-%d') + datetime.timedelta(days=15)).strftime('%Y-%m-%d')
            continue

        stories = news.news(display_output='full', company_tickers=ticker, pagesize=100, date_from=fromdate, date_to=todate)
        stories_df = process_stories(stories)
        df = pd.concat([df, stories_df]).drop_duplicates(subset=['title']).reset_index(drop=True)
        last_request_fromdate = fromdate
        fromdate = (df.iloc[-1, 0] - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    return df

tick_list = ['MSFT', 'JNJ', 'INTC', 'BA', 'UNH', 
             'JPM', 'V', 'PG', 'HD', 'CVX', 
             'MRK', 'KO', 'CSCO', 'MCD','WMT', 
             'CRM', 'DIS', 'VZ', 'NKE', 'AAPL', 
             'IBM', 'GS', 'HON', 'AXP', 'AMGN']
fromdate = "2019-01-01"
todate = "2023-05-03"

df_list = []
for ticker in tick_list:
    df_list.append( benzinga_call(ticker, fromdate, todate) )
df = pd.concat(df_list, axis=0)

df = df.sort_values(by='created')

df.to_csv('benzinga.csv', index=False)
