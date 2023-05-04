from etl.etl import ETL
from benzinga_tool import financial_data
from benzinga_tool import news_data
from benzinga_api.benzinga_api import * 

# inherit from ETL class
class Benzinga(ETL):
    def __init__(self, ticker, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticker = ticker

    def get(self):
       news = news_data.News(self.api_keys['Benzinga'])
       df = benzinga_call(news, self.ticker, self.start_day, self.end_day)
       return df
    
    def pull_benzinga_news(api_keys, tick_list, start_day, end_day):
        df_list = []
        for ticker in tick_list:
            news = Benzinga(api_keys = api_keys, ticker = ticker, start_day = start_day, end_day = end_day)
            df_list.append( news.get() )
        df = pd.concat(df_list, axis=0)
        df = df.sort_values(by='created')
        df.to_csv('benzinga.csv', index=False)