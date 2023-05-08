import pandas as pd
import glob
import os

class Preprocess():
    def __init__(self, path:str):
        self.benzinga = None
        self.macro = None
        self.youtube = None
        self.stock = None
        self.combination = None
        try:
            self.benzinga = pd.read_csv(os.path.join(path, 'benzinga_with_ratings.csv'))
        except FileNotFoundError:
            print('Benzinga file not found')
        try:
            self.macro = pd.read_csv(os.path.join(path, 'macro.csv'))
        except FileNotFoundError:
            print('Macro file not found')
        try:
            self.youtube = pd.read_csv(os.path.join(path, 'youtube_with_ratings.csv'))
        except FileNotFoundError:
            print('YouTube file not found')
        try:
            stock_file = glob.glob(os.path.join(path, '*_stock.csv'))[0]
            self.stock = pd.read_csv(stock_file)
        except IndexError:
            print('Stock file not found')

    def clean_benzinga(self):
        self.benzinga = self.benzinga[['created', 'benz_rate']]
        self.benzinga.dropna(subset=['benz_rate'], inplace=True)
        self.benzinga['benz_rate'] = self.benzinga['benz_rate'].astype(int)
        self.benzinga = self.benzinga.groupby('created')['benz_rate'].mean().reset_index()
        self.benzinga['benz_rate'] = self.benzinga['benz_rate'].round(4)
        self.benzinga = self.benzinga.rename(columns={'created': 'date'})
        self.benzinga['date'] = pd.to_datetime(self.benzinga['date']).dt.date
        print('Snapshot of benzinga data:')
        print(self.benzinga.head())
        print(f"Size:{self.benzinga.shape}")
    
    def clean_stock(self):
        exclude_cols = ['open', 'high', 'low','tic']
        self.stock = self.stock.drop(columns=exclude_cols)
        self.stock['date'] = pd.to_datetime(self.stock['date']).dt.date
        print('Snapshot of stock data:')
        print(self.stock.head())
        print(f"Size:{self.stock.shape}")

    def clean_macro(self):
        # Create a DataFrame with dates from 2023-02-02 to 2023-03-22 and interest rate = 4.58
        new_dates_1 = pd.date_range(start='2023-02-02', end='2023-03-22')
        new_data_1 = {'date': new_dates_1, 'interest_rates': 4.58}
        new_df_1 = pd.DataFrame(new_data_1)

        # Create a DataFrame with dates from 2023-03-23 to 2023-05-03 and interest rate = 4.83
        new_dates_2 = pd.date_range(start='2023-03-23', end='2023-05-03')
        new_data_2 = {'date': new_dates_2, 'interest_rates': 4.83}
        new_df_2 = pd.DataFrame(new_data_2)

        # Concatenate the two DataFrames
        new_df_12 = pd.concat([new_df_1, new_df_2], ignore_index=True)
        self.macro = pd.concat([self.macro, new_df_12], ignore_index=True)

        new_data = {'date': '2023-05-04',
                    'nfp': 0.0,
                    'cpi': 0.0,
                    'interest_rates': 5.08}
        new_df = pd.DataFrame(new_data, index=[0])
        self.macro = pd.concat([self.macro, new_df], ignore_index=True)
        self.macro = self.macro[['date', 'interest_rates']]
        self.macro['date'] = pd.to_datetime(self.macro['date']).dt.date
        print('Snapshot of macro data:')
        print(self.macro.head())
        print(f"Size:{self.macro.shape}")

    def merge_table(self):
        self.combination = pd.merge(self.stock, self.macro, on='date', how='left')
        self.combination = pd.merge(self.combination, self.benzinga, on='date', how='outer')
        self.combination = self.combination.sort_values(by='date').reset_index(drop=True)
        # Fill NA values using backward fill method for dates when market is closed
        columns_to_fill = [col for col in self.stock.columns if col not in ['date', 'benz_rate']]
        self.combination[columns_to_fill] = self.combination[columns_to_fill].fillna(method='bfill')
        # # Fill NA values using forward fill method for dates when no news created when market is open
        self.combination['benz_rate'] = self.combination['benz_rate'].fillna(method='ffill')
        self.combination['benz_rate'] = self.combination.groupby(['close', 'volume', 'day'])['benz_rate'].transform('mean')
        self.combination['benz_rate'] = self.combination['benz_rate'].round(3)
        self.combination = self.combination[self.combination['date'].isin(self.stock['date'])].sort_values(by='date').reset_index(drop=True)

    def export_to_csv(self):
        self.combination.to_csv("../data/cleaned_data.csv", index=False)



    # # this uncompleted function is used to merge tables based on user input
    # def merge_tables(self, table_list: list):
    #     for table in table_list:
    #         if hasattr(self, table):
    #             class_variable = getattr(self, table)
    #             if isinstance(class_variable, pd.DataFrame):
    #                 merged_dataframe = pd.concat([class_variable, class_variable], ignore_index=True)
    #                 setattr(self, table, merged_dataframe)