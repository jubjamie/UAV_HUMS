import tensorflow as tf
import pandas as pd
import os


for file in os.listdir("../../databin/test2/"):
    if file.endswith(".csv"):
        print(os.path.join("/databin/test2", file))
        # flight_df = pd.read_csv(pickFile(), header=0, index_col=None)