import pandas as pd
import numpy as np
from fastai.basic_data import DataBunch
from fastai.tabular import add_datepart
from sklearn import preprocessing
from torch.utils.data import Dataset

from lib.stock_controller import StockController


class StockDataset(Dataset):

    def __init__(self, X, tabular_data, y):
        self.X = X
        self.y = y
        self.tabular = tabular_data

    def __getitem__(self, i):
        return np.concatenate((self.X[i].flatten(), self.tabular[i].astype(int))), self.y[i]

    def __len__(self):
        return len(self.X)


class DataLoader(object):

    def __init__(self, stock_symbol, day_count, batch_size):
        self.stock_symbol = stock_symbol
        self.day_count = day_count
        self.batch_size = batch_size

    def _get_df_from_file(self):
        all_data_list = StockController.load_data_from_file(self.stock_symbol)
        df = pd.DataFrame(all_data_list).iloc[::-1]
        df["adj_close"] = df["adj_close"].astype(float)

        # add trend data
        df = df.set_index("date")
        df_trend = pd.read_csv(f"data/trends/{self.stock_symbol}.csv")
        df_merged = df.merge(df_trend.set_index("date"), how="inner", left_index=True, right_index=True)
        df = df_merged.reset_index()[["date", "adj_close", "bmw stock"]]

        add_datepart(df, "date")
        return df

    def get_databunch(self, valid_pct=0.1):
        df = self._get_df_from_file()

        data_normaliser = preprocessing.MinMaxScaler()
        data = data_normaliser.fit_transform(df["adj_close"].values.reshape(-1, 1))

        X = np.array([data[i: i + self.day_count].copy() for i in range(len(data) - self.day_count)])
        y = np.array([data[:, 0][i + self.day_count].copy() for i in range(len(data) - self.day_count)])
        tabular_data = np.array([df.drop(["adj_close", "Elapsed"], axis=1).iloc[i + self.day_count -1]
                                 for i in range(len(data)- self.day_count)])
        y = np.expand_dims(y, -1)

        n = int(len(X)*(1-valid_pct))

        train_ds = StockDataset(X[:n], tabular_data[:n], y[:n])
        valid_ds = StockDataset(X[n:], tabular_data[n:], y[n:])
        return DataBunch.create(train_ds, valid_ds, bs=self.batch_size)
