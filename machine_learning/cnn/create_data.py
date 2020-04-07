import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

LABELS_FILE = Path("../../data/labels.csv")
SOURCE_DIR = Path("../../data/csv")
DEST_DIR = Path("../../data/images/")
WINDOW_SIZE = 365 # one year
INVEST_DAYS = 14 # two weeks


class DataCreator(object):

    def __init__(self):
        self.stock_list = os.listdir(SOURCE_DIR)
        self.labels = pd.DataFrame(columns=['label'])

    @staticmethod
    def create_folder_if_not_exists(stock_name):
        if not os.path.exists(DEST_DIR/stock_name): os.mkdir(DEST_DIR/stock_name)

    @staticmethod
    def generate_stock_image(df, stock_name, iteration):
        window = df[iteration:iteration + WINDOW_SIZE]
        window.plot(kind='line', y='adj_close')
        ax1 = plt.axes()
        x_axis = ax1.axes.get_xaxis()
        x_axis.set_visible(False)
        plt.savefig(DEST_DIR / stock_name / f"{iteration}.png")
        plt.close()

    def get_roi(self, df, stock_name, iteration):
        """
        Returns the return on invest (ROI) for a specific stock within the next INVEST_DAYS days in percent
        :param df:
        :param iteration:
        :return:
        """
        start_price = df.iloc[iteration + WINDOW_SIZE]["adj_close"]
        end_price = df.iloc[iteration + WINDOW_SIZE + INVEST_DAYS]["adj_close"]
        self.labels.loc[str(DEST_DIR / stock_name / f"{iteration}.png")] = [(end_price - start_price) * 100 / start_price]

    def store_labels(self):
        self.labels.to_csv(LABELS_FILE)

    def create(self):
        for file in self.stock_list:
            print(f"Start creating images for {file}")
            df = pd.read_csv(SOURCE_DIR/file, index_col="date")
            df = df.reindex(index=df.index[::-1]) # reverse dataframe since the order is reversed

            if len(df) < (WINDOW_SIZE + INVEST_DAYS):
                print(f"Ignore: not enough data for {file}")
                continue

            stock_name = file.replace('.csv','')
            self.create_folder_if_not_exists(stock_name)
            i = 0
            while (i + WINDOW_SIZE + INVEST_DAYS) < len(df):
                self.generate_stock_image(df, stock_name, i)
                self.get_roi(df, stock_name, i)
                i = i + 1

        self.store_labels()

data_creator = DataCreator()
data_creator.create()
