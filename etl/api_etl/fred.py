from fredapi import Fred
from api_etl.etl import ETL

class Fredapi(ETL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fetch_macro_data(self):
        fred = Fred(api_key=self.api_keys["Fred"])
        # Non-Farm Payrolls (NFPs)
        nfp = fred.get_series("PAYEMS", self.start_day, self.end_day)
        nfp = nfp.resample("D").ffill().reset_index()
        nfp.columns = ["date", "nfp"]

        # Consumer Price Index (CPI)
        cpi = fred.get_series("CPALTT01USM657N", self.start_day, self.end_day)
        cpi = cpi.resample("D").ffill().reset_index()
        cpi.columns = ["date", "cpi"]

        # Interest Rates (Effective Federal Funds Rate)
        interest_rates = fred.get_series("FEDFUNDS", self.start_day, self.end_day)
        interest_rates = interest_rates.resample("D").ffill().reset_index()
        interest_rates.columns = ["date", "interest_rates"]

        macro_df = nfp.merge(cpi, on="date").merge(interest_rates, on="date")
        macro_df = macro_df.round(4)
        macro_df.to_csv('macro.csv', index=False)
        print('macro.csv created')
        return macro_df